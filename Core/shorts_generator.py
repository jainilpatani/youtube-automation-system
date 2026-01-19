import json
from google import genai
from config import GEMINI_API_KEY


def generate_shorts(script_text: str) -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    Create 3 YouTube Shorts concepts from this script:
    {script_text[:2000]}

    Return pure JSON with keys: hook, body, cta.
    """

    # ... inside generate_shorts function ...
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # <--- UPDATED
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )

    return json.loads(response.text)