"""
Number-word normalization for Russian and English.
Converts words like 'восьми', 'четыре', 'eight' → '8', '4', '8', etc.
"""

import re

RUSSIAN_NUM_WORDS = {
    "0": ["ноль", "нуля", "нулю", "нулём", "нуле"],
    "1": ["один", "одна", "одно", "одну", "одного", "одному", "одним", "одне", "первый", "первого"],
    "2": ["два", "две", "двух", "двум", "двумя", "второй", "второго"],
    "3": ["три", "трёх", "трем", "тремя", "трижды", "третий", "третьего"],
    "4": ["четыре", "четырёх", "четырём", "четырьмя", "четвертый", "четвертого"],
    "5": ["пять", "пяти", "пятому", "пятью", "пятый", "пятого"],
    "6": ["шесть", "шести", "шестому", "шестью", "шестой", "шестого"],
    "7": ["семь", "семи", "седьмой", "седьмого", "семью"],
    "8": ["восемь", "восьми", "восьмой", "восьмого", "восемью"],
    "9": ["девять", "девяти", "девятому", "девятью", "девятый", "девятого"],
    "10": ["десять", "десяти", "десятому", "десятью", "десятый", "десятого"],
}

ENGLISH_NUM_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
}

# Build a fast reverse dictionary for Russian forms
RUSSIAN_WORD_TO_DIGIT = {}
for digit, forms in RUSSIAN_NUM_WORDS.items():
    for form in forms:
        RUSSIAN_WORD_TO_DIGIT[form] = digit

def word_to_number(text: str) -> str:
    """
    Replace number words (Russian and English, any case/declension) with digits.
    """
    text = text.lower()
    # Replace Russian number words
    for word, digit in RUSSIAN_WORD_TO_DIGIT.items():
        text = re.sub(rf"\b{word}\b", digit, text, flags=re.IGNORECASE)
    # Replace English number words
    for word, digit in ENGLISH_NUM_WORDS.items():
        text = re.sub(rf"\b{word}\b", digit, text, flags=re.IGNORECASE)
    return text