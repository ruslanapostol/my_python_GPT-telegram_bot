from telegram import Update
from telegram.ext import ContextTypes
import logging
from telegram.constants import ChatAction
from telegram import InputFile
import os

logger = logging.getLogger(__name__)

async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/start received from {user.id} ({user.username})")

    gif_path = os.path.join(os.path.dirname(__file__), "..", "assets", "garfield.gif")
    await update.message.chat.send_action(action=ChatAction.UPLOAD_PHOTO)

    with open(gif_path, "rb") as gif_file:
        await update.message.reply_animation(
            animation=InputFile(gif_file),
            caption=(
                f"👋 Привет, {user.first_name}! Я Garfield-GPT-бот."
            )
        )
    await update.message.reply_text(
        "Вот что я умею:\n"
        "/random — случайный факт\n"
        "/gpt — задать вопрос ChatGPT\n"
        "/quiz — викторина\n"
        "/talk — диалог с известной личностью\n"
        "/help — справка"
    )

async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE):
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

async def about(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/about received by {update.effective_user.id}")
    await update.message.reply_text(
        "Этот бот использует ChatGPT для ответов на ваши вопросы и развлечений.\n"
        "Автор: apostolruslan\n"
        "Проект для обучения NLP и Telegram Bot API."
    )
