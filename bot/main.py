"""
Main entrypoint for the GPT-powered Telegram bot.
Loads handlers, configures logging, starts polling.
"""

import logging
from telegram.ext import Application, CommandHandler
from bot.config import TG_BOT_TOKEN
from bot.handlers.basic import start, help_command, about
from bot.handlers.random_fact import random_fact
from bot.handlers.gpt_chat import gpt_conversation
from bot.handlers.quiz import quiz_handler
from bot.handlers.talk import talk_handler

logging.basicConfig(
    format='%(asctime)s  [%(levelname)s]  %(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Entry point: sets up handlers, runs the bot, handles top-level errors."""
    logger.info("Starting bot...")

    try:
        application = Application.builder().token(TG_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about))
        application.add_handler(CommandHandler("random", random_fact))
        application.add_handler(gpt_conversation)
        application.add_handler(quiz_handler)
        application.add_handler(talk_handler)

        logger.info("Bot is polling for updates...")
        application.run_polling()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt).")
    except Exception:
        logger.exception("An error occurred while running the bot:")


if __name__ == "__main__":
    main()
