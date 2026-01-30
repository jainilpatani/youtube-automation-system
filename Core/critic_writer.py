from google import genai
import json
import ast
from config import GEMINI_API_KEY


def apply_critic_and_writer(draft_script: str):
    client = genai.Client(api_key=GEMINI_API_KEY)

    # 💎 PREMIUM MODEL
    model_name = "gemini-2.5-pro"

    # 1. CRITIC STEP
    critic_prompt = f"""
    You are a YouTube Script Critic. Review this script:
    {draft_script[:4000]}

    Identify 3 weaknesses in the 'Hook' and 'Retention'.
    """

    critique = "Standard Polish"
    try:
        critic_response = client.models.generate_content(
            model=model_name,
            contents=critic_prompt
        )
        critique = critic_response.text
    except Exception as e:
        print(f"⚠️ Critic skipped: {e}")

    # 2. WRITER STEP
    writer_prompt = f"""
    You are a Script Writer. Rewrite this script based on this critique: {critique}

    ORIGINAL SCRIPT:
    {draft_script[:4000]}

    Output structured JSON:
    {{
        "title": "Viral Title",
        "thumbnail": "Visual description",
        "keywords": ["tag1", "tag2"],
        "script": {{
            "00:00": {{ "visual": "...", "host": "..." }},
            "00:30": {{ "visual": "...", "host": "..." }}
        }}
    }}
    """

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=writer_prompt,
            config={"response_mime_type": "application/json"}
        )

        # Parse JSON safely
        try:
            return json.loads(response.text)
        except:
            return ast.literal_eval(response.text)

    except Exception as e:
        print(f"⚠️ Writer Error: {e}")
        return {"script": draft_script}