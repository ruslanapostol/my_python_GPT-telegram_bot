"""
Quiz service: loading, picking, and matching quiz questions/answers for the Telegram GPT bot.

- Loads quiz questions from JSON file.
- Picks random, non-repeating questions for the quiz handler.
- Implements "smart" answer checking (number words, fuzzy match, partial answers, unicode normalization).

Сервис викторины для Telegram-бота GPT:
- Загружает вопросы из JSON-файла.
- Выбирает случайные (неповторяющиеся) вопросы для викторины.
- Сравнивает ответы "умно": нормализация чисел, частичные ответы, поддержка опечаток, юникод.

Usage:
Imported as quiz_service singleton for use in handlers/quiz.py.
"""

import json
import os
import random
import logging
from typing import Optional, Dict, Any, List
import difflib
import re
import unicodedata
from bot.utils.numwords import word_to_number

logger = logging.getLogger(__name__)


class QuizService:
    """Service for loading, selecting, and checking quiz questions/answers."""
    def __init__(self, questions_file: str):
        self.questions_file = questions_file
        self.questions = self.load_questions()

    def load_questions(self) -> List[Dict[str, Any]]:
        """
        Loads quiz questions from a JSON file (expects a list of dicts with 'question' and 'answer').
        Returns an empty list on error.
        """
        try:
            with open(self.questions_file, "r", encoding="utf-8") as file:
                questions = json.load(file)
            if not isinstance(questions, list):
                raise ValueError("Quiz questions file does not contain a list.")
            logger.info(f"Loaded {len(questions)} questions from file")
            return questions
        except Exception as e:
            logger.error(f"Error loading quiz questions: {e}")
            return []

    def get_random_question(self, exclude: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """
        Return a random question not in the exclude list.
        If all questions have been asked, return None to indicate quiz completion.
        """
        if not self.questions:
            return None

        available = (
            [q for q in self.questions if q["question"] not in exclude]
            if exclude else self.questions
        )
        return random.choice(available) if available else None

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalizes text for comparison:
        - lowercases, strips
        - removes accents (Unicode normalization)
        - removes punctuation/non-alphanum
        """

        text = text.lower().strip()
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        return re.sub(r'[^a-zа-яё0-9 ]+', '', text, flags=re.IGNORECASE)

    @staticmethod
    def check_answer(user_answer: str, correct_answer: str) -> bool:
        """
        Smart matching:
        - Handles number words (e.g., "восьми", "eight" → 8)
        - Ignores case and punctuation
        - Accepts partial answers if all words are present
        - Fuzzy matches for minor typos
        """
        ua = word_to_number(user_answer)
        ca = word_to_number(correct_answer)

        ua_norm = QuizService.normalize(ua)
        ca_norm = QuizService.normalize(ca)

        if ua_norm == ca_norm:
            return True

        ua_words = set(ua_norm.split())
        ca_words = set(ca_norm.split())
        if ua_words and ua_words.issubset(ca_words):
            return True

        return difflib.SequenceMatcher(None, ua_norm, ca_norm).ratio() > 0.7


QUIZ_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "text/quiz_questions.json")
)
quiz_service = QuizService(QUIZ_FILE)
