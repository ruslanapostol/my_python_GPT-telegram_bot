from telegram import ReplyKeyboardMarkup, KeyboardButton


def persona_keyboard(persona_names: list[str], end_text="Закончить"):
    keyboard = [[KeyboardButton(name)] for name in persona_names]
    keyboard.append([KeyboardButton(end_text)])
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def end_keyboard(end_text="Закончить"):
    return ReplyKeyboardMarkup(
        [[KeyboardButton(end_text)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
