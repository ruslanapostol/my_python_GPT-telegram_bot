import logging
from telegram.ext import Application, CommandHandler
from config import TG_BOT_TOKEN

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s  [%(levelname)s]  %(name)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- Simple Command Handler Example ---
async def start(update, context):
    user = update.effective_user
    logger.info(f"/start received from user {user.id} ({user.username})")
    await update.message.reply_text(
        "👋 Привет! Я GPT-бот. Введите команду или вопрос."
        "\n\n👋 Hi! I'm a GPT-based bot. Send a command or question."
    )


# --- Main function to start the bot ---
def main():
    logger.info("Starting bot...")

    try:
        # Create an application instance with bot token
        application = Application.builder().token(TG_BOT_TOKEN).build()

        # Register command handler
        application.add_handler(CommandHandler("start", start))

        # Start polling (listening for messages)
        logger.info("Bot is polling for updates...")
        application.run_polling()
    except Exception as e:
        logger.exception("An error occurred while running the bot:")


if __name__ == "__main__":
    main()
