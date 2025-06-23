"""
Loads sensitive credentials for the bot (Telegram token, OpenAI token)
from a .env file in the project root using python-dotenv.
If tokens are missing, raises a clear error.
"""


import os
from dotenv import load_dotenv

load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHATGPT_TOKEN = os.getenv("CHATGPT_TOKEN")

if not all([TG_BOT_TOKEN, CHATGPT_TOKEN]):
    raise ValueError("❌ Please set both TG_BOT_TOKEN and CHATGPT_TOKEN in your .env file.")



