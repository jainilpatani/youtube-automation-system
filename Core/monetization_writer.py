import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def rewrite_for_clarity_and_cpm(original_script, critic_feedback):
    prompt = f"""
You are a PROFESSIONAL YouTube Scriptwriter specializing in:
- High CPM niches
- Fast monetization approval
- Simple, clear English
- Global audience understanding

ORIGINAL SCRIPT:
\"\"\"
{original_script}
\"\"\"

CRITIC FEEDBACK:
\"\"\"
{critic_feedback}
\"\"\"

REWRITE RULES (MANDATORY):
- Keep the idea 100% original
- Make language simple (no jargon)
- Short sentences
- Clear cause → effect explanations
- Remove hype, fear, or misleading claims
- Improve hook clarity
- Insert soft CTAs naturally
- Avoid sensitive financial promises
- Sound human, calm, confident

TARGET:
- 800–1200 words
- High retention
- Advertiser-safe
- Monetization-friendly
- Easy for voiceover

OUTPUT FORMAT:
1. Final Title (1)
2. Thumbnail Text (max 4 words)
3. Final Script
4. SEO Keywords (10–12)
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1600
    )

    return response["choices"][0]["message"]["content"]
