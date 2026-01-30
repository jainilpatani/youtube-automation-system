import os
import json
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure AI
genai.configure(api_key=GEMINI_API_KEY)
UPLOADS_DIR = "uploads"


def find_latest_project():
    all_projects = []
    for root, dirs, files in os.walk(UPLOADS_DIR):
        if "long" in dirs:
            all_projects.append(root)
    if not all_projects: return None
    return sorted(all_projects, key=os.path.getmtime, reverse=True)[0]


def generate_viral_shorts(script_text):
    print("🧠 Consulting the AI Director...")

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
    {script_text[:4000]}

    Return the response as a raw JSON list of objects:
    [
        {{"title": "Viral Concept 1", "script": "🪝 HOOK\\n...\\n📝 BODY\\n...\\n📣 CTA\\n..."}},
        {{"title": "Viral Concept 2", "script": "..."}},
        {{"title": "Viral Concept 3", "script": "..."}}
    ]
    """

    try:
        # ✅ FIX: Updated to the new model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Clean the response to ensure it's valid JSON
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return []


def run():
    # 1. Find Folder
    target_folder = find_latest_project()
    if not target_folder:
        print("❌ No project found.")
        return
    print(f"📂 Targeting: {os.path.basename(target_folder)}")

    # 2. Read Script
    script_path = os.path.join(target_folder, "long", "01_script.txt")
    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    # 3. Generate Creative Shorts
    shorts_data = generate_viral_shorts(script_text)

    if not shorts_data:
        print("⚠️ AI generation failed. Try again.")
        return

    # 4. Save
    shorts_dir = os.path.join(target_folder, "shorts")
    os.makedirs(shorts_dir, exist_ok=True)

    for i, short in enumerate(shorts_data):
        file_path = os.path.join(shorts_dir, f"short_{i + 1}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(short, f, indent=4)
        print(f"   ✨ Created Creative Short #{i + 1}")

    print("\n🎉 Done! Refresh your Dashboard.")


if __name__ == "__main__":
    run()