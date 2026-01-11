from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def critic_review(text: str) -> str:
    """
    Lightweight critic agent used for fast sanity checks.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict YouTube content quality critic."},
            {"role": "user", "content": text}
        ],
        temperature=0.4,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()