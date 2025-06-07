from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters
import logging
from bot.services.quiz_service import quiz_service, QuizService

logger = logging.getLogger(__name__)
ASKING = range(1)


async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    question = quiz_service.get_random_question()
    if not question:
        logger.error(f"No quiz questions available for user {user.id} ({user.username})")
        await update.message.reply_text("Извините, вопросы для викторины сейчас недоступны.")
        return ConversationHandler.END
    context.user_data["current_quiz"] = question
    logger.info(f"/quiz started by {user.id} ({user.username}) - Вопрос: {question['question']}")
    await update.message.reply_text(
        f"Викторина! 🧠\n\n{question['question']}\n(Ответьте или /cancel для отмены)"
    )
    return ASKING


async def quiz_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    question = context.user_data.get("current_quiz")
    user_answer = update.message.text.strip().lower()
    if not question:
        logger.error(f"Quiz state lost for user {user.id} ({user.username})")
        await update.message.reply_text("Что-то пошло не так. Попробуйте /quiz ещё раз.")
        return ConversationHandler.END
    is_correct = QuizService.check_answer(user_answer, question["answer"])

    msg = "✅ Верно! Молодец." if is_correct else f"❌ Неверно. Правильный ответ: {question['answer']}"
    logger.info(
        f"User {user.id} ({user.username}): Q='{question['question']}' | A='{user_answer}' | Correct={is_correct}")
    await update.message.reply_text(msg)
    return ConversationHandler.END


async def quiz_cancel(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/quiz cancelled by {user.id} ({user.username})")
    await update.message.reply_text("Викторина отменена.")
    return ConversationHandler.END


quiz_handler = ConversationHandler(
    entry_points=[CommandHandler("quiz", quiz_start)],
    states={ASKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_check)]},
    fallbacks=[CommandHandler("cancel", quiz_cancel)],
)
