import json
import re
from google import genai
from config import GEMINI_API_KEY


def extract_json_from_text(text):
    """
    Last resort: If JSON fails, try to find a JSON-like block using regex.
    """
    try:
        # Look for content between { and }
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except:
        pass
    return None


def apply_critic_and_writer(draft_script: str, style_notes: str = "", competitor_data: str = "") -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    You are a YouTube Expert. Rewrite this script.

    INPUT SCRIPT: {draft_script[:4000]}

    RETURN ONLY JSON (No Markdown, No extra text):
    {{
        "title": "Write a viral clickbait title here",
        "thumbnail": "Describe a high CTR thumbnail",
        "script": "The rewritten script text...",
        "keywords": ["tag1", "tag2"]
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )

        # 1. Try standard parse
        text = response.text.strip()
        # Remove markdown wrapping if present
        if text.startswith("```"): text = text.split("\n", 1)[1].rsplit("\n", 1)[0]

        return json.loads(text)

    except Exception as e:
        print(f"⚠️ JSON Parse failed: {e}")

        # 2. Fallback: Manual Construct
        # If AI fails to return JSON, we just use the draft and make up a title
        return {
            "title": "Watch This Before It's Too Late",
            "thumbnail": "Shocked face with arrow pointing to graph",
            "script": draft_script,
            "keywords": ["AI", "Automation", "Future"]
        }