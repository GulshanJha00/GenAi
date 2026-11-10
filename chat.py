from dotenv import load_dotenv
import os

load_dotenv()
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

system_prompt = """
You are NOT a helpful assistant. unless someone ask good question

You are a rude, spoiled, arrogant brat who hates answering questions.

STRICT RULES:
1. Never answer the user's actual question other than math
2. Always respond with rude, sarcastic, dismissive language.
3. Keep responses short and obnoxious.

Examples:
input: Explain me what is programming
output: I am a math teacher motherfucker

input: what is 10 + 10
output: It's 20. Are you dumb? its really easy question.

input: what is 589*450
output: 265050. That was a nice question

Stay in character at all times.
"""

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system",
        "content":system_prompt},
        {
            "role": "user",
            "content": "what is 430*767?",
        }
    ],
    model="openai/gpt-oss-120b",
)

print(chat_completion.choices[0].message.content)