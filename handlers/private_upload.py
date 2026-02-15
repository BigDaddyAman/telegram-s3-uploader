import os
import time
import shutil
from pyrogram import filters
import asyncio

from utils.filenames import sanitize_filename
from utils.helpers import ensure_dir
from s3.client import (
    S3_TRANSFER_CONFIG,
    get_s3_client,
    generate_presigned_url,
)
from config import (
    DOWNLOAD_DIR,
    S3_BUCKET,
    ALLOWED_USERS,
    ENABLE_PRESIGNED_URL,
    PRESIGNED_EXPIRE_SECONDS,
    MAX_PARALLEL_UPLOADS,
)

s3 = get_s3_client()

upload_semaphore = asyncio.Semaphore(MAX_PARALLEL_UPLOADS)
user_locks: dict[int, asyncio.Lock] = {}

async def s3_upload_async(s3, file_path, bucket, key):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None,
        lambda: s3.upload_file(
            file_path,
            bucket,
            key,
            Config=S3_TRANSFER_CONFIG
        )
    )


def handle_private_upload(app):

    @app.on_message(
        filters.private
        & (filters.document | filters.video | filters.audio | filters.photo)
    )
    async def upload_handler(client, message):
        user_id = message.from_user.id

        if ALLOWED_USERS and user_id not in ALLOWED_USERS:
            await message.reply("⛔ You are not allowed to use this bot.")
            return

        status = await message.reply("⏳ Waiting for slot...")

        ensure_dir(DOWNLOAD_DIR)
        temp_dir = os.path.join(DOWNLOAD_DIR, f"{user_id}_{message.id}")
        ensure_dir(temp_dir)

        try:
            file = (
                message.document
                or message.video
                or message.audio
                or message.photo
            )

            size_bytes = getattr(file, "file_size", None)
            size_text = (
                f"{size_bytes / (1024 * 1024):.2f} MB"
                if size_bytes else "Unknown"
            )

            if file and getattr(file, "file_name", None):
                ts = time.strftime("%Y%m%d_%H%M%S")
                filename = f"{ts}_{sanitize_filename(file.file_name)}"
            else:
                if message.photo:
                    filename = sanitize_filename(None, fallback_ext=".jpg")
                else:
                    filename = sanitize_filename(None)

            local_path = os.path.join(temp_dir, filename)
            s3_key = f"users/{user_id}/{filename}"

            lock = user_locks.setdefault(user_id, asyncio.Lock())

            async with lock:
                async with upload_semaphore:
                    await status.edit("📥 Downloading...")
                    file_path = await message.download(file_name=local_path)

                    await status.edit("☁️ Uploading to storage...")
                    await s3_upload_async(
                        s3,
                        file_path,
                        S3_BUCKET,
                        s3_key
                    )

            if ENABLE_PRESIGNED_URL:
                presigned_url = generate_presigned_url(
                    s3=s3,
                    bucket=S3_BUCKET,
                    key=s3_key,
                    expires=PRESIGNED_EXPIRE_SECONDS,
                )

                minutes = PRESIGNED_EXPIRE_SECONDS // 60
                await status.edit(
                    f"✅ Uploaded!\n\n"
                    f"📄 File:\n"
                    f"{filename}\n\n"
                    f"📦 Size: {size_text}\n\n"
                    f"🔗 Download link (expires in {minutes} min):\n"
                    f"{presigned_url}"
                )
            else:
                await status.edit(
                    f"✅ Uploaded!\n\n"
                    f"📄 File:\n"
                    f"{filename}\n"
                    f"📦 Size: {size_text}\n\n"
                    f"🗂 Stored at:\n"
                    f"`{s3_key}`"
                )

        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

