"""
Conversation handler for /talk command.
Lets the user choose a famous persona and chat as if the personaa were replying.
Handles persona selection, main conversation loop, and graceful exit.
"""

import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
)
from telegram.constants import ParseMode
from bot.services.persona_service import persona_service
from bot.services.openai_service import ask_chatgpt
from bot.utils.keyboards import persona_keyboard, end_keyboard

logger = logging.getLogger(__name__)

CHOOSING_PERSONA, TALKING = range(2)


async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for /talk. Shows available personas to the user and starts the conversation."""
    personas = persona_service.get_personas()
    if not personas:
        logger.error(f"No personas available for user {update.effective_user.id} ({update.effective_user.username})")
        await update.message.reply_text("Персонажи недоступны.", parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    persona_names = [p["name"] for p in personas]
    context.user_data.clear()
    await update.message.reply_text(
        "Выберите персонажа для общения:",
        reply_markup=persona_keyboard(persona_names)
    )
    return CHOOSING_PERSONA


async def persona_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the user's persona selection and transitions to the chat state."""
    persona_name = update.message.text.strip()
    if persona_name == "Закончить":
        return await talk_cancel(update, context)

    prompt = persona_service.get_prompt_by_name(persona_name)
    if not prompt:
        await update.message.reply_text(
            "Выберите персонажа из списка или нажмите 'Закончить'.",
            parse_mode=ParseMode.HTML
        )
        return CHOOSING_PERSONA

    context.user_data["persona_name"] = persona_name
    context.user_data["persona_prompt"] = prompt

    await update.message.reply_text(
        f"Теперь вы общаетесь с персонажем: <b>{persona_name}</b>\n\n"
        "Напишите сообщение, и персонаж ответит вам как будто это он!",
        parse_mode=ParseMode.HTML,
        reply_markup=end_keyboard()
    )
    return TALKING


async def persona_talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's messages to the selected persona, routes via ChatGPT, and replies.
     If no persona is selected, restarts the persona selection process.
    """
    text = update.message.text.strip()
    if text == "Закончить":
        return await talk_cancel(update, context)

    prompt = context.user_data.get("persona_prompt")
    persona_name = context.user_data.get("persona_name", "???")
    if not prompt:
        await update.message.reply_text(
            "Персонаж не выбран. Используйте /talk для начала.",
            parse_mode=ParseMode.HTML
        )
        personas = persona_service.get_personas()
        persona_names = [p["name"] for p in personas]
        await update.message.reply_text(
            "Выберите персонажа для общения:",
            reply_markup=persona_keyboard(persona_names)
        )
        return CHOOSING_PERSONA

    user_input = update.message.text.strip()
    full_prompt = f"{prompt}\n\nВопрос пользователя: {user_input}"

    logger.info(f"Persona chat ({persona_name}): {user_input}")

    answer = await ask_chatgpt(full_prompt)
    await update.message.reply_text(answer, parse_mode=ParseMode.HTML)
    return TALKING


async def talk_cancel(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Gracefully ends the conversation and removes the custom keyboard."""
    await update.message.reply_text(
        "Режим общения с персонажем завершён.",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Register the talk conversation handler in the main.py file:
talk_handler = ConversationHandler(
    entry_points=[CommandHandler("talk", talk_start)],
    states={
        CHOOSING_PERSONA: [MessageHandler(filters.TEXT & ~filters.COMMAND, persona_chosen)],
        TALKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, persona_talk)]
    },
    fallbacks=[CommandHandler("cancel", talk_cancel)],
)
