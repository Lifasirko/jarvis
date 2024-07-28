from openai import OpenAI
import os

from config.settings import CHAT_GPT_API_KEY

api_key = CHAT_GPT_API_KEY
client = OpenAI(api_key=api_key)


def get_chatgpt_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
