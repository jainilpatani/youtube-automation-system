# Core/critic_writer.py
import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def apply_critic_and_writer(
        draft_script: str,
        style_notes: str = "",
        competitor_data: str = ""  # <--- NEW INPUT
) -> dict:
    # Build context string
    context_block = ""
    if style_notes:
        context_block += f"\nPASSED WINNING PATTERNS:\n{style_notes}\n"
    if competitor_data:
        context_block += f"\nREAL-TIME COMPETITOR DATA:\n{competitor_data}\n"

    prompt = f"""
    You are TWO EXPERTS working together.

    INPUT SCRIPT:
    \"\"\"
    {draft_script}
    \"\"\"

    {context_block}

    TASK:
    1. Analyze the competitor data. If there are "OUTLIER" videos, steal their angle (but not their words).
    2. Rewrite the script to match the viral energy of the top competitors.
    3. Ensure the tone is calm and educational (no hype).

    OUTPUT FORMAT (JSON):
    {{
        "title": "Viral title based on competitor analysis",
        "thumbnail": "Visual description",
        "script": "The full rewritten script...",
        "keywords": ["tag1", "tag2"]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.4
    )

    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {"script": draft_script, "title": "Error", "keywords": []}