"""
Asynchronous wrapper for OpenAI ChatGPT API.
Provides a single ask_chatgpt(prompt) function to get a response from GPT.
"""

import openai
import os
import logging

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("CHATGPT_TOKEN")
if not OPENAI_API_KEY:
    logger.warning("CHATGPT_TOKEN environment variable not set!")



async def ask_chatgpt(prompt: str, model="gpt-3.5-turbo") -> str:
    """
    Sends a prompt to OpenAI's GPT API and returns the generated response.
    :param prompt: User's question or input string.
    :param model: Model name (default: "gpt-3.5-turbo").
    :return: GPT response as string, or error message.
    """
    try:
        client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "Ошибка при обращении к GPT."