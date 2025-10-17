import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔑 Sozlamalar
BOT_TOKEN = os.getenv("8171012194:AAFU2F55ZyOkaQuTj21CU4wnHRf20k6dXFI")  # Token Render’da saqlanadi
ADMIN_ID = 6621350057  # O'zingizning Telegram ID'ingizni yozing

videos = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Bu Zapal Bot.\n"
        "🎥 Video olish uchun /get <raqam>\n"
        "📤 Video qo‘shish uchun (faqat admin): /save <raqam> + video"
    )

async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Bu buyruq faqat admin uchun!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("❗ Foydalanish: /save <raqam>")
        return

    code = context.args[0]

    if update.message.reply_to_message and update.message.reply_to_message.video:
        videos[code] = update.message.reply_to_message.video.file_id
        await update.message.reply_text(f"✅ Video saqlandi: {code}")
    else:
        await update.message.reply_text("❗ Video yuboring va unga javoban /save <raqam> yozing")

async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗ Foydalanish: /get <raqam>")
        return

    code = context.args[0]

    if code in videos:
        await update.message.reply_video(videos[code])
    else:
        await update.message.reply_text("❌ Bunday kodli video topilmadi.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(8171012194:AAFU2F55ZyOkaQuTj21CU4wnHRf20k6dXFI).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("save", save_video))
    app.add_handler(CommandHandler("get", get_video))
    app.run_polling()
