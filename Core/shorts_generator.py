# Core/shorts_generator.py
import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_shorts(script_text: str) -> dict:
    prompt = f"""
Create YouTube Shorts components from the script below.

SCRIPT:
\"\"\"
{script_text}
\"\"\"

Return ONLY valid JSON:

{{
  "hook": "string",
  "loop": "string",
  "cta": "string"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
