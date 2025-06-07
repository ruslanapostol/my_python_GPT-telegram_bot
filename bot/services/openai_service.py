import openai
import os


openai.api_key = os.getenv("CHATGPT_TOKEN")
print("DEBUG TOKEN: ", repr(openai.api_key))


async def ask_chatgpt(prompt: str, model="gpt-3.5-turbo") -> str:
    try:
        client = openai.AsyncOpenAI(api_key=os.getenv("CHATGPT_TOKEN"))
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("DEBAG OPENAI ERROR:", e)
        return "Ошибка при обращении к GPT."
