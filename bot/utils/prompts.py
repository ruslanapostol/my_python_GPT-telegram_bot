"""
Prompts for the /paraphrase command in multiple languages.
These templates guide GPT to rephrase text in a friendly, clear, and psychologically aware manner,
using simple language and examples where possible.

Промпты для команды /paraphrase на разных языках.
Эти шаблоны просят GPT переформулировать текст дружелюбно, понятно, с примерами и простыми словами.
"""

PARAPHRASE_PROMPTS = {
    "en": (
        "Please rephrase this text so it’s clear, easy to understand, and feels friendly—like you’re explaining it in a calm, supportive way to someone who might not be familiar with the topic. "
        "If possible, use simple language, examples, or analogies to make it more approachable:\n\n"
        "{txt}"
    ),
    "ru": (
        "Переформулируй этот текст так, чтобы он был понятен и звучал по-дружески — представь, что объясняешь человеку, который с этим впервые сталкивается. "
        "Если получится, используй простые слова, сравнения или аналогии для ясности:\n\n"
        "{txt}"
    ),
    "es": (
        "Reformula este texto para que sea claro, fácil de entender y suene amistoso, como si se lo explicaras a alguien que no conoce bien el tema. "
        "Si puedes, utiliza un lenguaje sencillo, ejemplos o comparaciones para hacerlo más accesible:\n\n"
        "{txt}"
    ),
    "ro": (
        "Reformulează acest text ca să fie clar, ușor de înțeles și să sune prietenos—ca și cum l-ai explica cuiva care nu știe prea multe despre subiect. "
        "Dacă se poate, folosește un limbaj simplu, exemple sau analogii ca să fie mai accesibil:\n\n"
        "{txt}"
    ),
}

DEFAULT_PARAPHRASE_PROMPT = (
    "Rephrase this text so it’s clear, friendly, and easy to understand, as if you’re calmly explaining it to someone new to the subject. "
    "If you can, use simple language, examples, or analogies:\n\n"
    "{txt}"
)