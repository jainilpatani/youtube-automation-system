from google import genai
from config import GEMINI_API_KEY


def rewrite_for_clarity_and_cpm(original_script, critic_feedback):
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    Rewrite for high CPM.
    Script: {original_script}
    Feedback: {critic_feedback}
    """

    # ... inside rewrite_for_clarity_and_cpm function ...
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # <--- UPDATED
        contents=prompt
    )
    return response.text