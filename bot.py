import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
FREE_CHANNEL_URL = os.environ.get("FREE_CHANNEL_URL", "https://t.me/your_free_channel")

WELCOME_TEXT = (
    "Hello, brother 👋\n\n"
    "Sorry for delay in text.\n"
    "If you want free signal, follow our free channel 👇"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Free Channel", url=FREE_CHANNEL_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Any message other than /start gets the welcome too
    await start(update, context)

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
