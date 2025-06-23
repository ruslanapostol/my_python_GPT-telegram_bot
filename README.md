# GPT Telegram Bot (MVP) / Телеграм-бот с GPT (MVP)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)

A simple Telegram bot powered by OpenAI's GPT and written in Python 3.  
Бот для Telegram на Python 3 с поддержкой OpenAI GPT. Модульная структура, легко расширяется.

---

## About NLP Features

**This bot isn’t just a simple GPT wrapper — it includes real NLP/ML logic!**  
My `/paraphrase` command is a practical showcase of NLP:  
it detects the language of your input (Russian, English, Spanish, Romanian) and asks GPT to generate a human-sounding paraphrase.  
_This is my “psychologist-who-codes-NLP” moment_ 😄

---

## Features / Функционал

- `/start` — Welcome message / Приветствие  
- `/help` — List of commands / Доступные команды  
- `/about` — Project info / О проекте  
- `/random` — Random fact / Случайный факт  
- `/gpt` — ChatGPT Q&A / Вопросы к GPT  
- `/quiz` — Quiz / Викторина  
- `/talk` — Persona dialog / Диалог с персонажем  
- `/paraphrase` — **NLP feature!** Paraphrase any text in Russian, English, Spanish, or Romanian using GPT  
  _Моя первая NLP-функция: перефразирует текст на русском, английском, испанском или румынском (авто-определение языка)_

---

## Installation / Установка

```bash
git clone https://github.com/ruslanapostol/my_python_GPT-telegram_bot.git
cd my_python_GPT-telegram_bot
poetry install
```

---

## Usage / Использование
	1.	Add environment variables:
    TG_BOT_TOKEN=ваш_telegram_token
    CHATGPT_TOKEN=ваш_openai_token


	2.	Run the bot:
    Запуск:
    poetry run python bot/main.py  или  python -m bot.main

---

## NLP: Paraphrase Command / Перефразирование
	•	/paraphrase — my showcase of NLP-in-action!
	•	Detects input language automatically (ru/en/es/ro).
	•	Sends your text to GPT and returns a fresh, natural-sounding paraphrase.
	•	Try several in a row, or send /cancel to exit.

---

## Handler Overview / Обзор обработчиков
	•	handlers/random_fact.py — Sends a random fact from file
    Отправляет случайный факт из файла
	•	handlers/gpt_chat.py — Q&A with ChatGPT
    Вопрос-ответ с ChatGPT
	•	handlers/quiz.py — Quiz logic
    Викторина (вопросы, ответы, баллы)
	•	handlers/talk.py — Persona/character dialog
    Диалог с известной личностью
	•	handlers/paraphrase.py — NLP-powered paraphrasing
    Перефразирование текста с автоопределением языка (GPT)

---

## Data Files / Данные

    personas.json:

    List of available personas for /talk. Each persona has a name and a prompt that sets up ChatGPT’s character.
    Список доступных персонажей для команды /talk. Каждый объект должен содержать поля name (имя) и prompt (стиль/характер для ChatGPT).

    quiz_questions.json:

    Quiz questions for /quiz. Each entry has a question and the correct answer.
    Вопросы для викторины /quiz. Каждый объект — это пара question (вопрос) и answer (правильный ответ).

---

## Project Structure / Структура проекта

    bot/
      assets/          # Facts, quiz questions, personas (JSON, txt, png)
      handlers/        # Command handlers
      services/        # Service logic (OpenAI, personas, quiz)
      utils/           # Helpers, keyboards
      main.py          # Entry point


---

## License / Лицензия

    Apache License 2.0
---

## Author / Автор

    Ruslan Apostol
    Python/NLP student, polyglot, psychologist
    apostolruslan.python@gmail.com
---

