# Core/script_generator.py
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_original_script(topic: str) -> str:
    prompt = f"""
Explain the following topic clearly and calmly.

Topic:
{topic}

Rules:
- Simple English
- Short spoken sentences
- Educational tone
- No hype or fear
- No promises

Length:
800–1200 words
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=1400
    )

    return response.choices[0].message.content.strip()
