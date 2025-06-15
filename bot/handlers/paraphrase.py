"""
/paraphrase command handler for Telegram bot.
Supports Russian, English, Spanish, Romanian. Automatically detects input language.
Lets user paraphrase as many texts as they want in a row, until they send /cancel.

Команда /paraphrase: определяет язык (русский, английский, испанский, румынский)
и генерирует перефразированный вариант через GPT. Можно отправлять несколько текстов подряд.
"""

import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
from bot.services.openai_service import ask_chatgpt
from langdetect import detect, LangDetectException
from bot.utils.prompts import PARAPHRASE_PROMPTS, DEFAULT_PARAPHRASE_PROMPT

logger = logging.getLogger(__name__)

PARAPHRASE_ASKING = range(1)


async def paraphrase_start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Entry point for /paraphrase command. Prompts the user to input text.
    Точка входа для /paraphrase. Просит пользователя ввести текст.
    """
    await update.message.reply_text(
        "Введите текст для перефразирования (русский, английский, испанский, румынский).\n"
        "Можете отправлять несколько текстов подряд. Для выхода — /cancel.",
        reply_markup=ReplyKeyboardRemove()
    )
    return PARAPHRASE_ASKING


async def paraphrase_process(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handles user input: detects language and requests GPT paraphrase.
    Обрабатывает текст пользователя: определяет язык и отправляет запрос к GPT.
    """
    user_text = update.message.text.strip()
    if not user_text:
        await update.message.reply_text("Пожалуйста, введите текст для перефразирования.")
        return PARAPHRASE_ASKING

    try:
        language = detect(user_text)
        logger.info(f"Detected language: {language}")
    except LangDetectException:
        language = "en"
        logger.info("Language detection failed, defaulting to English.")

    if language.startswith("ru"):
        lang_key = "ru"
    elif language.startswith("es"):
        lang_key = "es"
    elif language.startswith("ro"):
        lang_key = "ro"
    else:
        lang_key = "en"

    prompt_template = PARAPHRASE_PROMPTS.get(lang_key, DEFAULT_PARAPHRASE_PROMPT)
    prompt = prompt_template.format(txt=user_text)

    logger.info(f"/paraphrase: Lang={lang_key}, Text='{user_text}'")

    await update.message.reply_text("⏳ GPT формулирует перефразированный текст...")

    try:
        response = await ask_chatgpt(prompt)
        await update.message.reply_text(response.strip())
    except Exception as e:
        logger.error(f"Error during GPT paraphrasing: {e}")
        await update.message.reply_text("Произошла ошибка при обращении к GPT.")

    await update.message.reply_text(
        "Введите следующий текст для перефразирования или /cancel для выхода."
    )
    return PARAPHRASE_ASKING


async def paraphrase_cancel(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Graceful cancel of the paraphrase conversation.
    Корректно завершает диалог перефразирования.
    """
    await update.message.reply_text(
        "Перефразирование отменено. 😊\nСпасибо за использование /paraphrase!",
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


paraphrase_handler = ConversationHandler(
    entry_points=[CommandHandler("paraphrase", paraphrase_start)],
    states={
        PARAPHRASE_ASKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, paraphrase_process)]
    },
    fallbacks=[CommandHandler("cancel", paraphrase_cancel)],
)
