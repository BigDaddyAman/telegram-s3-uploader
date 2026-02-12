import os
import time
import shutil
from pyrogram import filters

from s3.client import get_s3_client, generate_presigned_url
from utils.filenames import sanitize_filename
from utils.helpers import ensure_dir
from config import (
    DOWNLOAD_DIR,
    S3_BUCKET,
    ALLOWED_USERS,
    ENABLE_PRESIGNED_URL,
    PRESIGNED_EXPIRE_SECONDS,
)

s3 = get_s3_client()


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

        status = await message.reply("📥 Downloading...")

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

            if file and getattr(file, "file_name", None):
                ts = time.strftime("%Y%m%d_%H%M%S")
                filename = f"{ts}_{sanitize_filename(file.file_name)}"
            else:
                if message.photo:
                    filename = sanitize_filename(None, fallback_ext=".jpg")
                else:
                    filename = sanitize_filename(None)

            local_path = os.path.join(temp_dir, filename)

            file_path = await message.download(file_name=local_path)

            s3_key = f"users/{user_id}/{filename}"

            await status.edit("☁️ Uploading to storage...")
            s3.upload_file(file_path, S3_BUCKET, s3_key)

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
                    f"🔗 Download link (expires in {minutes} min):\n"
                    f"{presigned_url}"
                )
            else:
                await status.edit(
                    f"✅ Uploaded!\n\n"
                    f"🗂 Stored at:\n"
                    f"`{s3_key}`"
                )

        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
