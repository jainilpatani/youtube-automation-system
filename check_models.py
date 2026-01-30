# check_models.py
import os
from google import genai
from config import GEMINI_API_KEY


def check():
    print("👨‍⚕️ Running Model Doctor...")
    if not GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY not found in config.py")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        print("📡 Connecting to Google AI...")
        # List all available models
        models = list(client.models.list(config={"page_size": 100}))

        print("\n✅ AVAILABLE MODELS (Copy one of these exact names):")
        found_flash = False
        for m in models:
            # We only care about generateContent models
            if "generateContent" in m.supported_generation_methods:
                clean_name = m.name.split("/")[-1]  # removes 'models/' prefix
                print(f"   • {clean_name}")
                if "flash" in clean_name:
                    found_flash = True

        if not found_flash:
            print("\n⚠️ WARNING: No 'flash' model found. Your API key might be restricted.")

    except Exception as e:
        print(f"\n❌ CONNECTION ERROR: {e}")


if __name__ == "__main__":
    check()