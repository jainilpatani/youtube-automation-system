# diagnose.py
import os
from google import genai
from config import GEMINI_API_KEY


def diagnose():
    print("👨‍⚕️ DIAGNOSTIC TOOL RUNNING...")
    print("--------------------------------")

    if not GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY is missing from config.py")
        return

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        # Fetch list of models
        response = client.models.list(config={"page_size": 50})

        print("✅ SUCCESS! Here are your available models:")
        print("(Copy the EXACT string inside the quotes)")
        print("--------------------------------")

        count = 0
        for m in response:
            # Try to get the name safely
            name = getattr(m, 'name', None)
            if not name:
                # Fallback for older library versions
                name = str(m).split("name='")[-1].split("'")[0]

            # Clean up the name (remove 'models/' prefix if present)
            clean_name = name.replace("models/", "")

            # Only show generation models (filtering out embedding/tuning models)
            if "generate" in str(m) or "gemini" in clean_name:
                print(f"🔹 {clean_name}")
                count += 1

        if count == 0:
            print("⚠️ No models found. This usually means your API Key has no access to Generative Language API.")
            print("   -> Go to https://aistudio.google.com/app/apikey to check your key.")

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("   -> This usually means your 'google-genai' library is too old or the API Key is invalid.")


if __name__ == "__main__":
    diagnose()