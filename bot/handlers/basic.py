from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/start received from {user.id} ({user.username})")
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}! Я GPT-бот. Вот что я умею:\n"
        "/random — случайный факт\n"
        "/gpt — задать вопрос ChatGPT\n"
        "/quiz — викторина\n"
        "/talk — диалог с известной личностью\n"
        "/help — справка"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/help received by {update.effective_user.id}")
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — начать работу\n"
        "/random — случайный факт\n"
        "/gpt — спросить ChatGPT\n"
        "/quiz — викторина\n"
        "/talk — диалог с известной личностью\n"
        "/help — эта справка"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/about received by {update.effective_user.id}")
    await update.message.reply_text(
        "Этот бот использует ChatGPT для ответов на ваши вопросы и развлечений.\n"
        "Автор: apostolruslan\n"
        "Проект для обучения NLP и Telegram Bot API."
    )
