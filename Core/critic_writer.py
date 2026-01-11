# Core/critic_writer.py
import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def apply_critic_and_writer(draft_script: str, style_notes: str) -> dict:
    prompt = f"""
You are TWO experts working together.

CRITIC:
- Improve retention
- Remove hype and fear
- Ensure advertiser safety

WRITER:
- Simple English
- Short spoken sentences
- Calm, confident tone

STYLE NOTES FROM PAST BEST CONTENT:
{style_notes}

INPUT SCRIPT:
\"\"\"
{draft_script}
\"\"\"

Return ONLY valid JSON in this format:

{{
  "title": "string",
  "thumbnail": "string",
  "final_script": "string",
  "seo_keywords": ["string", "string"]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1400,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
