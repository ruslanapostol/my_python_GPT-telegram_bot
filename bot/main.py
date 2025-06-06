import logging
from telegram.ext import Application, CommandHandler
from config import TG_BOT_TOKEN
from handlers.basic import start, help_command, about
from handlers.random_fact import random_fact

logging.basicConfig(
    format='%(asctime)s  [%(levelname)s]  %(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting bot...")

    try:
        application = Application.builder().token(TG_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about))
        application.add_handler(CommandHandler("random", random_fact))

        logger.info("Bot is polling for updates...")
        application.run_polling()
        
    except Exception as e:
        logger.exception("An error occurred while running the bot:")


if __name__ == "__main__":
    main()
