"""
Helper functions for creating custom reply keyboards for the Telegram bot.
Вспомогательные функции для создания пользовательских клавиатур.
"""

from telegram import ReplyKeyboardMarkup, KeyboardButton
from bot.utils.constants import RETRY_BUTTON_LABEL, NEW_Q_BUTTON_LABEL, END_QUIZ_LABEL


def persona_keyboard(persona_names: list[str], end_text="Закончить"):
    """
      Creates a keyboard for persona selection:
      """
    keyboard = [[KeyboardButton(name)] for name in persona_names]
    keyboard.append([KeyboardButton(end_text)])
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def end_keyboard(end_text=END_QUIZ_LABEL):
    """Simple keyboard with a single 'End' button."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton(end_text)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def quiz_retry_keyboard():
    """
       Клавиатура с кнопками 'Еще попытка' и 'Новый вопрос' для режима викторины.
       """
    return ReplyKeyboardMarkup(
        [[KeyboardButton(RETRY_BUTTON_LABEL), KeyboardButton(NEW_Q_BUTTON_LABEL)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def quiz_question_keyboard():
    """
    Клавиатура для основного вопроса викторины — только кнопка 'Закончить викторину'.
    """
    return ReplyKeyboardMarkup(
        [[KeyboardButton(END_QUIZ_LABEL)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )