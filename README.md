# my_python_GPT-telegram_bot

A Telegram bot powered by ChatGPT, built with Python and [python-telegram-bot](https://python-telegram-bot.org), managed with [Poetry](https://python-poetry.org/).

Телеграм-бот с поддержкой ChatGPT, написанный на Python с использованием [python-telegram-bot](https://python-telegram-bot.org) и управляемый с помощью [Poetry](https://python-poetry.org/).

---

## Features / Основные возможности

- Integrates with ChatGPT (OpenAI API)
- Several bot commands: `/random`, `/gpt`, `/talk`, `/quiz` and more
- Environment variable support with `.env`
- Modular and easy-to-extend codebase
- (Optional) **NLP Features:** Translation, summarization, sentiment analysis, and more

- Интеграция с ChatGPT (OpenAI API)
- Несколько команд бота: `/random`, `/gpt`, `/talk`, `/quiz` и другие
- Работа с переменными окружения через `.env`
- Модульная и легко расширяемая архитектура
- (Опционально) **NLP-функции:** перевод, резюмирование, анализ настроения и др.

---

## Requirements / Требования

- Python 3.10+ (рекомендуется Python 3.13)
- Poetry (для управления зависимостями)
- Telegram Bot Token ([получить через @BotFather](https://core.telegram.org/bots#botfather))
- OpenAI API Key ([зарегистрироваться здесь](https://platform.openai.com/signup))

---

## Quick Start / Быстрый старт

1. **Clone the repository / Клонируйте репозиторий**
    ```bash
    git clone https://github.com/yourusername/my_python_GPT-telegram_bot.git
    cd my_python_GPT-telegram_bot
    ```

2. **Install dependencies with Poetry / Установите зависимости через Poetry**
    ```bash
    poetry install
    ```

3. **Copy `.env.example` to `.env` and set your secrets / Скопируйте `.env.example` в `.env` и укажите свои токены**
    ```bash
    cp .env.example .env
    ```
    Fill in your `TELEGRAM_TOKEN` and `OPENAI_API_KEY` inside `.env`.
    Впишите свои значения для `TELEGRAM_TOKEN` и `OPENAI_API_KEY` в файл `.env`.

4. **Run the bot / Запустите бота**
    ```bash
    poetry run python -m bot.main
    ```

---

## Environment Variables / Переменные окружения

`.env` file should contain your tokens:
`.env` файл должен содержать ваши токены: