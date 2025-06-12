"""
Helper functions for creating custom reply keyboards for the Telegram bot.
Вспомогательные функции для создания пользовательских клавиатур.
"""

from telegram import ReplyKeyboardMarkup, KeyboardButton


def persona_keyboard(persona_names: list[str], end_text="Закончить"):
    """
      Creates a keyboard for persona selection:
      :param persona_names: List of persona names (Список имен персонажей)
      :param end_text: Text for the "End" button (Текст кнопки "Закончить")
      :return: ReplyKeyboardMarkup object
      """
    keyboard = [[KeyboardButton(name)] for name in persona_names]
    keyboard.append([KeyboardButton(end_text)])
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def end_keyboard(end_text="Закончить"):
    """
       Simple keyboard with a single 'End' button.
       :param end_text: Text for the button (Текст кнопки)
       :return: ReplyKeyboardMarkup object
       """
    return ReplyKeyboardMarkup(
        [[KeyboardButton(end_text)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def quiz_retry_keyboard():
    """
       Клавиатура с кнопками 'Еще попытка' и 'Новый вопрос' для режима викторины.
       :return: ReplyKeyboardMarkup object
       """
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Еще попытка"), KeyboardButton("Новый вопрос")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def quiz_question_keyboard():
    """
    Клавиатура для основного вопроса викторины — только кнопка 'Закончить викторину'.
    :return: ReplyKeyboardMarkup object
    """
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Закончить викторину")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )