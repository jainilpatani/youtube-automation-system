from google import genai
from config import GEMINI_API_KEY


def critic_review(text: str) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)

    # ... inside critic_review function ...
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # <--- UPDATED
        contents=f"Critique this script for retention: {text[:3000]}"
    )
    return response.text