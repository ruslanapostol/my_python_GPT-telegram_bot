import logging
import random

from telegram import Update, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from bot.services.quiz_service import quiz_service
from bot.utils.constants import (
    RETRY_BUTTON_LABEL,
    NEW_Q_BUTTON_LABEL,
    RETRY_BUTTONS,
    NEW_Q_BUTTONS,
    END_QUIZ_BUTTONS,
)
from bot.utils.keyboards import quiz_retry_keyboard, quiz_question_keyboard
from bot.utils.texts import (
    QUESTION_INTROS,
    COMPLIMENTS,
    FAILURES,
    HIGH_SCORE,
    LOW_SCORE,
    FAREWELLS,
)

logger = logging.getLogger(__name__)

ASKING, RETRY = range(2)


def get_farewell(score: int, total: int) -> str:
    """Returns a dynamic farewell/summary message based on score."""
    if score == 0:
        return random.choice(LOW_SCORE)
    elif score == total and total > 0:
        return random.choice(HIGH_SCORE)
    elif score >= max(2, total // 2):
        return random.choice(FAREWELLS)
    else:
        return random.choice(LOW_SCORE)


async def send_perfect_score_image(update: Update) -> None:
    """Sends a celebratory GIF or image for perfect quiz results."""
    try:
        logger.info("Trying to send perfect score GIF...")
        with open("bot/assets/rolling_garfield.gif", "rb") as gif:
            logger.info("GIF file opened successfully, sending...")
            await update.message.reply_animation(
                gif,
                caption="Ты победил(а) эту викторину. Бедные вопросы даже не успели испугаться!",
                parse_mode=ParseMode.HTML,
            )
    except Exception as e:
        logger.warning(f"Could not send winner gif: {e}")


async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the quiz session and sends the first question.
    Clears user session data to prevent interference with previous quiz sessions.
    """
    user = update.effective_user
    context.user_data.clear()
    context.user_data['score'] = 0
    context.user_data['asked_questions'] = []
    logger.info(f"Quiz started by {user.id} ({user.username})")
    return await send_new_question(update, context)


async def send_new_question(update: Update, context: ContextTypes.DEFAULT_TYPE,
                            last_answer_correct: bool = False) -> int:
    """Selects and sends a new quiz question, handles compliments, and manages quiz ending."""
    asked_questions = context.user_data.get('asked_questions', [])
    question = quiz_service.get_random_question(exclude=asked_questions)

    if question is None:
        score = context.user_data.get('score', 0)
        total = len(asked_questions)
        if score == total and total > 0:
            await send_perfect_score_image(update)
            return ConversationHandler.END
        farewell = get_farewell(score, total)
        await update.message.reply_text(
            f"Викторина завершена! Ваш итоговый счет: {score} из {total}.\n{farewell}",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    if last_answer_correct:
        compliment = random.choice(COMPLIMENTS)
        await update.message.reply_text(
            f"✅ {compliment} Твой счет: {context.user_data['score']}.",
            reply_markup=ReplyKeyboardRemove()
        )

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
    """Checks the user's answer and handles correct/incorrect flow.
    Allow quitting the quiz via keywords"""
    user = update.effective_user
    user_answer = update.message.text.strip()
    text = user_answer.lower()

    quit_commands = {
        "закончить викторину", "/cancel", "стоп", "выход", "end quiz", "quit"
    }.union(END_QUIZ_BUTTONS)
    if text in quit_commands:
        logger.info(f"User {user.id} quit the quiz with: {user_answer}")
        return await quiz_cancel(update, context)

    question = context.user_data.get('current_question')
    if not question:
        logger.error(f"Missing question state for user {user.id} ({user.username})")
        return await send_new_question(update, context)

    correct_answer = question['answer']
    is_correct = quiz_service.check_answer(user_answer, correct_answer)
    logger.info(f"User {user.id} answered '{user_answer}' (expected '{correct_answer}'): {is_correct}")

    if is_correct:
        context.user_data["score"] += 1
        return await send_new_question(update, context, last_answer_correct=True)
    else:
        failure = random.choice(FAILURES)
        await update.message.reply_text(
            f"❌ {failure} Можешь попробовать ещё раз или взять новый вопрос.",
            reply_markup=quiz_retry_keyboard()
        )
        return RETRY


async def quiz_retry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the user's choice to retry the same question or get a new one."""
    text = update.message.text.strip().lower()
    if text in END_QUIZ_BUTTONS:
        return await quiz_cancel(update, context)

    user = update.effective_user
    logger.info(f"Retry choice by {user.id}: {text}")

    if text in RETRY_BUTTONS:
        question = context.user_data['current_question']
        await update.message.reply_text(
            f"Попробуй еще раз!\nВопрос: {question['question']}",
            reply_markup=quiz_question_keyboard()
        )
        return ASKING

    if text in NEW_Q_BUTTONS:
        return await send_new_question(update, context)

    await update.message.reply_text(
        f"Пожалуйста, выберите '{RETRY_BUTTON_LABEL}' или '{NEW_Q_BUTTON_LABEL}'.",
        reply_markup=quiz_retry_keyboard()
    )
    return RETRY


async def quiz_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ends the quiz and displays the final score with a dynamic message."""
    user = update.effective_user
    score = context.user_data.get('score', 0)
    total_questions = len(context.user_data.get('asked_questions', []))
    logger.info(f"Quiz cancelled by {user.id}. Final score: {score}")

    if score == total_questions and total_questions > 0:
        await send_perfect_score_image(update)

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
