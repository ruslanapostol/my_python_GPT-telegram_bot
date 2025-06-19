"""
Random fact handler module.
Loads fun facts from a text file and replies with a random one.
"""

import random
from telegram import Update
from telegram.ext import ContextTypes
import logging
import os

logger = logging.getLogger(__name__)

FACTS_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "text/facts.txt")
)

def load_facts():
    """
    Loads facts from a text file.
    Returns a list of non-empty lines.
    """
    try:
        logger.debug(f"Looking for text/facts.txt at {FACTS_PATH}")
        with open(FACTS_PATH, "r", encoding="utf-8") as file:
            facts = [line.strip() for line in file if line.strip()]
            logger.info(f"Loaded {len(facts)} facts from file")
            return facts
    except Exception as e:
        logger.error("Could not load facts from file: %s", e)
        return ["Не удалось загрузить факты."]


FACTS = load_facts()


async def random_fact(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /random command.
    Sends a random fact from the loaded list.
    """
    fact = random.choice(FACTS)
    logger.info(f"/random fact sent to {update.effective_user.id}")
    await update.message.reply_text(f"🧠 {fact}")
