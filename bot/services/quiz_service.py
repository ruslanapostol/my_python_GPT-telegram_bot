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

    def get_random_question(self) -> Optional[Dict[str, Any]]:
        if not self.questions:
            return None
        return random.choice(self.questions)

    @staticmethod
    def check_answer(user_answer: str, correct_answer: str) -> bool:
        return user_answer.strip().lower() == correct_answer.strip().lower()


QUIZ_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "quiz_questions.json")
)
quiz_service = QuizService(QUIZ_FILE)
