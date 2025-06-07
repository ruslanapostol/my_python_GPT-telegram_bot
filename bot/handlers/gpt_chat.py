from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.services.openai_service import ask_chatgpt

ASKING = range(1)


async def gpt_command(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши свой вопрос для ChatGPT или /cancel для выхода:")
    return ASKING


async def gpt_ask(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.reply_text("Запрашиваю ответ у ChatGPT...")
    answer = await ask_chatgpt(user_input)
    await update.message.reply_text(answer)
    return ConversationHandler.END


async def cancel(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог с ChatGPT отменён.")
    return ConversationHandler.END


# The ConversationHandler object that gets registered in main.py
gpt_conversation = ConversationHandler(
    entry_points=[CommandHandler("gpt", gpt_command)],
    states={
        ASKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_ask)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
