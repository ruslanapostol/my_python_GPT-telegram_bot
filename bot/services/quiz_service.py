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
    def __init__(self, questions_file: str):
        self.questions_file = questions_file
        self.questions = self.load_questions()

    def load_questions(self) -> List[Dict[str, Any]]:
        """Loads quiz questions from a JSON file."""
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
        text = text.lower().strip()
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        return re.sub(r'[^a-zа-яё0-9]+', '', text, flags=re.IGNORECASE)

    @staticmethod
    def check_answer(user_answer: str, correct_answer: str) -> bool:
        ua = word_to_number(user_answer)
        ca = word_to_number(correct_answer)
        ua = QuizService.normalize(ua)
        ca = QuizService.normalize(ca)

        if ua == ca:
          return True

        ua_words = set(re.findall(r'[a-zа-яё0-9]+', ua))
        ca_words = set(re.findall(r'[a-zа-яё0-9]+', ca))
        if ua_words and ua_words.issubset(ca_words):
            return True

        return difflib.SequenceMatcher(None, ua, ca).ratio() > 0.77


QUIZ_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "quiz_questions.json")
)
quiz_service = QuizService(QUIZ_FILE)
