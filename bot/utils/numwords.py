"""
Number-word normalization for Russian and English.
Converts words like 'восьми', 'четыре', 'eight' → '8', '4', '8', etc.
"""

import unicodedata
import re

RUSSIAN_NUM_WORDS = {
    "0": ["ноль"],
    "1": ["один", "одна", "одно", "одну"],
    "2": ["два", "две", "двух", "двум", "двумя"],
    "3": ["три", "трёх", "тремя", "трое", "триёх"],
    "4": ["четыре", "четыр", "четырех", "четырём", "четвёртый", "четвертый"],
    "5": ["пять", "пяти", "пятью"],
    "6": ["шесть", "шести", "шестью"],
    "7": ["семь", "семи", "семью"],
    "8": ["восемь", "восьм", "восьми", "восьмой", "восьмью"],
    "9": ["девять", "девяти", "девятью"],
    "10": ["десять", "десяти", "десятью"]
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
    # ...add more if needed
}

def word_to_number(text: str) -> str:
    """
    Replaces number words with their digit equivalents (Russian and English).
    Handles phrases like 'восемь', 'eight', etc.
    """
    words = text.lower().split()
    converted = []
    for w in words:
        if w in RUSSIAN_NUM_WORDS:
            converted.append(RUSSIAN_NUM_WORDS[w])
        elif w in ENGLISH_NUM_WORDS:
            converted.append(ENGLISH_NUM_WORDS[w])
        else:
            converted.append(w)
    return ' '.join(converted)