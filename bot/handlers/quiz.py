import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)
from bot.services.quiz_service import quiz_service
from bot.utils.keyboards import quiz_retry_keyboard

logger = logging.getLogger(__name__)
ASKING, RETRY = range(2)


async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the quiz session and sends the first question."""
    user = update.effective_user
    context.user_data.clear()
    context.user_data['score'] = 0
    context.user_data['asked_questions'] = []
    logger.info(f"Quiz started by {user.id} ({user.username})")
    return await send_new_question(update, context)


async def send_new_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Selects and sends a new quiz question without repeats."""
    asked = context.user_data.get('asked_questions', [])

    question = quiz_service.get_random_question(exclude=asked)
    if question is None:
        score = context.user_data.get('score', 0)
        await update.message.reply_text(
            f"Викторина завершена! Ваш итоговый счет: {score}",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    asked.append(question["question"])
    context.user_data["asked_questions"] = asked
    context.user_data["current_question"] = question

    await update.message.reply_text(
        f"Вопрос: {question['question']}",
        reply_markup=ReplyKeyboardRemove()
    )
    return ASKING


async def quiz_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Checks the user's answer and either advances the quiz or shows retry options."""
    user = update.effective_user
    user_answer = update.message.text.strip()
    question = context.user_data.get('current_question')

    if not question:
        logger.error(f"Missing question state for user {user.id} ({user.username})")
        return await send_new_question(update, context)

    correct_answer = question['answer']
    is_correct = quiz_service.check_answer(user_answer, correct_answer)
    logger.info(
        f"User {user.id} answered '{user_answer}' (expected '{correct_answer}'): {is_correct}"
    )

    if is_correct:
        context.user_data["score"] += 1
        await update.message.reply_text(
            f"✅ Верно! Ваш счет: {context.user_data['score']}.\nСледующий вопрос:",
            reply_markup=ReplyKeyboardRemove()
        )
        return await send_new_question(update, context)
    else:
        await update.message.reply_text(
            "❌ Неправильно. Попробуй еще или возьми новый вопрос.",
            reply_markup=quiz_retry_keyboard()
        )
        return RETRY


async def quiz_retry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the user's choice to retry the same question or get a new one."""
    user = update.effective_user
    choice = update.message.text.strip().lower()
    logger.info(f"Retry choice by {user.id}: {choice}")

    if choice in ("еще попытка", "ещё попытка"):
        question = context.user_data['current_question']
        await update.message.reply_text(
            f"Попробуй еще раз!\nВопрос: {question['question']}",
            reply_markup=ReplyKeyboardRemove()
        )
        return ASKING

    if choice == "новый вопрос":
        return await send_new_question(update, context)

    await update.message.reply_text(
        "Пожалуйста, выберите 'Еще попытка' или 'Новый вопрос'.",
        reply_markup=quiz_retry_keyboard()
    )
    return RETRY


async def quiz_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ends the quiz and displays the final score."""
    user = update.effective_user
    score = context.user_data.get('score', 0)
    logger.info(f"Quiz cancelled by {user.id}. Final score: {score}")
    await update.message.reply_text(
        f"Викторина завершена! Ваш результат: {score}",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


quiz_handler = ConversationHandler(
    entry_points=[CommandHandler("quiz", quiz_start)],
    states={
        ASKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_check)],
        RETRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_retry)],
    },
    fallbacks=[CommandHandler("cancel", quiz_cancel)],
)
