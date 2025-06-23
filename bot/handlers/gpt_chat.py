"""
GPT Chat handler module.
Handles the /gpt command for interactive ChatGPT Q&A.
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.services.openai_service import ask_chatgpt

ASKING = range(1)


async def gpt_command(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Напиши свой вопрос для ChatGPT или /cancel для выхода:"
    )
    return ASKING


async def gpt_ask(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Handles a user question, sends it to ChatGPT, and replies with the answer.
    Handles errors gracefully.
    """
    user_input = update.message.text
    await update.message.reply_text("Запрашиваю ответ у ChatGPT...")

    try:
        answer = await ask_chatgpt(user_input)
        if not answer:
            raise ValueError("Empty answer from ChatGPT API")
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(
            "⚠️ Ошибка при запросе к ChatGPT. Попробуйте ещё раз позже."
        )
        print(f"[gpt_ask] OpenAI API error: {e}")
    return ConversationHandler.END


async def cancel(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """Handles user cancellation (/cancel command)."""
    await update.message.reply_text("Диалог с ChatGPT отменён.")
    return ConversationHandler.END


#  Register the conversation handler (used in main.py)
gpt_conversation = ConversationHandler(
    entry_points=[CommandHandler("gpt", gpt_command)],
    states={
        ASKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_ask)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
