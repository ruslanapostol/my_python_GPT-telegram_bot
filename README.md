# GPT Telegram Bot (MVP) / Телеграм-бот с GPT (MVP)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)

A simple Telegram bot powered by OpenAI's GPT and written in Python 3.  
Бот для Telegram на Python 3 с поддержкой OpenAI GPT. Модульная структура, легко расширяется.

---

## Table of Contents

| English                       | Русский                         |
|-------------------------------|---------------------------------|
| [Features](#features)         | [Функционал](#функционал)       |
| [Installation](#installation) | [Установка](#установка)         |
| [Usage](#usage)               | [Использование](#использование) |
| [Handlers](#handlers)         | [Обработчики](#обработчики)     |
| [Structure](#structure)       | [Структура](#структура)         |
| [License](#license)           | [Лицензия](#лицензия)           |
| [Author](#author)             | [Автор](#автор)                 |

---

## Features / Функционал

- `/start` — Welcome message / Приветствие
- `/help` — List of commands / Доступные команды
- `/about` — Project info / О проекте
- `/random` — Random fact / Случайный факт
- `/gpt` — ChatGPT Q&A / Вопросы к GPT
- `/quiz` — Quiz / Викторина
- `/talk` — Persona dialog / Диалог с персонажем

---

## Installation / Установка

```bash
git clone https://github.com/ruslanapostol/my_python_GPT-telegram_bot.git
cd my_python_GPT-telegram_bot
poetry install
```

---

## Usage / Использование

1. **Add environment variables:**  
   Скопируйте `.env.example` → `.env` и добавьте ваши токены:
   ```
   TG_BOT_TOKEN=ваш_telegram_token
   CHATGPT_TOKEN=ваш_openai_token
   ```

2. **Run the bot:**  
   Запуск:

   ```bash
   poetry run python bot/main.py
   ```
   # или
   ```
   python -m bot.main
   ```

---

## Handler Overview / Обзор обработчиков

- `handlers/random_fact.py` — Sends a random fact from file  
  Отправляет случайный факт из файла

- `handlers/gpt_chat.py` — Q&A with ChatGPT  
  Вопрос-ответ с ChatGPT

- `handlers/quiz.py` — Quiz logic  
  Викторина (вопросы, ответы, баллы)

- `handlers/talk.py` — Persona/character dialog  
  Диалог с известной личностью

---

## Project Structure / Структура проекта

```
bot/
  assets/          # Facts, quiz questions, personas (JSON, txt, png)
  handlers/        # Command handlers
  services/        # Service logic (OpenAI, personas, quiz)
  utils/           # Helpers, keyboards
  main.py          # Entry point
```

---


## Data Files / Данные

1. `personas.json`
   List of available personas for /talk. Each persona has a name and a prompt that sets up ChatGPT’s character.
Format:
[
  {
    "name": "Persona Name",
    "prompt": "Instructions for ChatGPT in the persona's style"
  },
  ...
]
Example:
[
  {
    "name": "Albert Einstein",
    "prompt": "You are Albert Einstein, famous physicist. Always answer in the first person..."
  }
]
Русский:
Список доступных персонажей для команды /talk. 
Каждый объект должен содержать поля name (имя) и prompt (стиль/характер для ChatGPT).

2.` quiz_questions.json`
Quiz questions for /quiz. Each entry has a question and the correct answer.
Format:
[
  {
    "question": "Your question here",
    "answer": "Correct answer"
  },
  ...
]
Example:
[
  {
    "question": "What is the capital of France?",
    "answer": "Paris"
  },
  {
    "question": "2 + 2?",
    "answer": "4"
  }
]
Русский:
Вопросы для викторины /quiz. Каждый объект — это пара question (вопрос) и answer (правильный ответ).


## License / Лицензия

Apache License 2.0

---

## Author / Автор

Ruslan Apostol  
Python/NLP student, polyglot, psychologist  
apostolruslan.python@gmail.com