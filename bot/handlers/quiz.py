import logging
import random
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
from bot.utils.texts import QUESTION_INTROS, COMPLIMENTS, FAILURES, FAREWELLS, HIGH_SCORE, LOW_SCORE


logger = logging.getLogger(__name__)

ASKING, RETRY = range(2)

def get_farewell(score: int, total: int) -> str:
    """
    Returns a dynamic farewell/summary message based on score.
     - Perfect or >= half correct: High score praise.
    - Less than half: Gentle encouragement.
    - Zero: Motivational message.
    """
    if score == 0:
        return random.choice(LOW_SCORE)
    elif score == total:
        return random.choice(HIGH_SCORE)
    elif score >= total // 2:
        return random.choice(HIGH_SCORE)
    else:
        return random.choice(LOW_SCORE)

async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the quiz session and sends the first question.
    Clears user session data to prevent interference with previous quizz sessions.
    """
    user = update.effective_user
    context.user_data.clear()
    context.user_data['score'] = 0
    context.user_data['asked_questions'] = []
    logger.info(f"Quiz started by {user.id} ({user.username})")
    return await send_new_question(update, context)


async def send_new_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Selects and sends a new quiz question without repeats."""
    asked_questions = context.user_data.get('asked_questions', [])
    question = quiz_service.get_random_question(exclude=asked_questions)
    if question is None:
        score = context.user_data.get('score', 0)
        total_questions = len(asked_questions)
        farewell = get_farewell(score, total_questions)
        await update.message.reply_text(
             f"Викторина завершена! Ваш итоговый счет: {score} из {total_questions}.\n{farewell}",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    asked_questions.append(question["question"])
    context.user_data["asked_questions"] = asked_questions
    context.user_data["current_question"] = question

    intro = random.choice(QUESTION_INTROS)
    await update.message.reply_text(
        f"{intro}\nВопрос: {question['question']}",
        reply_markup=ReplyKeyboardRemove()
    )
    return ASKING


async def quiz_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Checks the user's answer and handles correct/incorrect flow."""
    user = update.effective_user
    user_answer = update.message.text.strip()
    question = context.user_data.get('current_question')

    if not question:
        logger.error(f"Missing question state for user {user.id} ({user.username})")
        return await send_new_question(update, context)

    correct_answer = question['answer']
    is_correct = quiz_service.check_answer(user_answer, correct_answer)
    logger.info( f"User {user.id} answered '{user_answer}' (expected '{correct_answer}'): {is_correct}")

    if is_correct:
        context.user_data["score"] += 1
        compliment = random.choice(COMPLIMENTS)
        await update.message.reply_text(
             f"✅ {compliment} Твой счет: {context.user_data['score']}.\nСледующий вопрос:",
            reply_markup=ReplyKeyboardRemove()
        )
        return await send_new_question(update, context)
    else:
        failure = random.choice(FAILURES)
        await update.message.reply_text(
            f"❌ {failure} Можешь попробовать ещё раз или взять новый вопрос.",
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
    """Ends the quiz and displays the final score with a dynamic message."""
    user = update.effective_user
    score = context.user_data.get('score', 0)
    total_questions = len(context.user_data.get('asked_questions', []))
    logger.info(f"Quiz cancelled by {user.id}. Final score: {score}")

    farewell = get_farewell(score, total_questions)

    await update.message.reply_text(
        f"Викторина завершена! Ваш результат: {score} из {total_questions}.\n{farewell}",
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
