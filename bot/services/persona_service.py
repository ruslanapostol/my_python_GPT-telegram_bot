import json
import os
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class PersonaService:
    def __init__(self, personas_file: str):
        self.personas_file = personas_file
        self.personas = self.load_personas()

    def load_personas(self) -> List[Dict[str, str]]:
        try:
            with open(self.personas_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("Personas JSON must contain a list.")
            logger.info(f"Loaded {len(data)} personas from file")
            return data
        except Exception as e:
            logger.error(f"Error loading personas: {e}")
            return []

    def get_personas(self) -> List[Dict[str, str]]:
        return self.personas

    def get_prompt_by_name(self, name: str) -> Optional[str]:
        for persona in self.personas:
            if persona.get("name") == name:
                return persona.get("prompt")
        return None


PERSONAS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "personas.json")
)

persona_service = PersonaService(PERSONAS_FILE)
