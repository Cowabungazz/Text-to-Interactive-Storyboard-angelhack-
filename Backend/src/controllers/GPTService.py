import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_lesson_from_text(prompt: str) -> dict:
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```json"):
        content = content[len("```json"):].strip()
    if content.endswith("```"):
        content = content[:-len("```")].strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {content}")
        raise
