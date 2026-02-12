from pyrogram import filters
from config import ALLOWED_USERS

def handle_start(app):

    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message):
        user_id = message.from_user.id

        if user_id not in ALLOWED_USERS:
            await message.reply("⛔ You are not allowed to use this bot.")
            return

        await message.reply(
            "✅ Bot is alive!\n\n"
            "📤 Send me any file and I will upload it to storage."
        )
