import json
import os
import random
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class QuizService:
    def __init__(self, questions_file: str):
        self.questions_file = questions_file
        self.questions = self.load_questions()

    def load_questions(self) -> List[Dict[str, Any]]:
        """
        Loads quiz questions from a JSON file.
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

    def get_random_question(self, exclude: Optional[str] = None) -> Optional[Dict[str, Any]]:
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
    def check_answer(user_answer: str, correct_answer: str) -> bool:
        """
               Accepts:
                1. Full exact match: "Уильям Шекспир"
                2. Single-word match: either "Уильям" or "Шекспир"
               Rejects any multi-word answer that isn't the exact full name.
               """
        ua = user_answer.strip().lower()
        ca = correct_answer.strip().lower()

        if ua == ca:
            return True

        ua_words = ua.split()
        ca_words = ca.split()
        if len(ua_words) == 1 and ua_words[0] in ca_words:
            return True
        return False


QUIZ_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "quiz_questions.json")
)
quiz_service = QuizService(QUIZ_FILE)
