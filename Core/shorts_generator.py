import google.generativeai as genai
import json
from config import GEMINI_API_KEY

# Configure AI
genai.configure(api_key=GEMINI_API_KEY)


def generate_shorts(long_script_text):
    """
    Generates 3 Creative Viral Shorts using Gemini AI.
    """
    print("📱 Generating Viral Shorts Concepts...")

    prompt = f"""
    You are a viral content strategist. I have a long YouTube script.
    I need you to write 3 DISTINCT YouTube Shorts scripts based on it.

    For each Short, you MUST use this exact format with emojis:

    🪝 HOOK
    (A scroll-stopping visual or sentence to grab attention instantly)

    📝 BODY
    (The core value proposition, fast-paced and punchy)

    📣 CTA
    (A direct call to action to watch the main video)

    ---

    Here is the Long Script to adapt:
    {long_script_text[:5000]}

    Return the response as a raw JSON list of objects:
    [
        {{"title": "Viral Concept 1", "script": "🪝 HOOK\\n...\\n📝 BODY\\n...\\n📣 CTA\\n..."}},
        {{"title": "Viral Concept 2", "script": "..."}},
        {{"title": "Viral Concept 3", "script": "..."}}
    ]
    """

    try:
        # Use the Flash model for speed and low cost
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Clean the response to ensure it's valid JSON
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)

    except Exception as e:
        print(f"⚠️ Shorts Generation Failed: {e}")
        # Fallback if AI fails (prevents crash)
        return [
            {"title": "Error generating shorts", "script": "Could not generate shorts. Check API Key."}
        ]