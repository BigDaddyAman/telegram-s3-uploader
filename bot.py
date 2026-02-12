from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.private_upload import handle_private_upload
from handlers.start import handle_start

app = Client(
    "telegram-s3-uploader",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

handle_start(app)
handle_private_upload(app)
handle_private_upload(app)

print("🚀 Bot started")
app.run()
