import os
import json
import random
from Core import shorts_generator

UPLOADS_DIR = "uploads"


def find_latest_project():
    """Finds the most recent project folder."""
    all_projects = []
    for root, dirs, files in os.walk(UPLOADS_DIR):
        if "long" in dirs and "shorts" in dirs:
            all_projects.append(root)

    if not all_projects:
        return None

    # Sort by creation time (newest first)
    all_projects.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return all_projects[0]


def repair_shorts():
    # 1. Find the target folder
    target_folder = find_latest_project()
    if not target_folder:
        print("❌ No video projects found to repair.")
        return

    print(f"🔧 Repairing Shorts for: {os.path.basename(target_folder)}")

    # 2. Read the Main Script
    script_path = os.path.join(target_folder, "long", "01_script.txt")
    if not os.path.exists(script_path):
        print("❌ Main script not found. Cannot generate shorts.")
        return

    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    # 3. Generate New Shorts
    print("⏳ Generating 3 Viral Shorts (this may take a moment)...")
    try:
        shorts_data = shorts_generator.generate_shorts(script_text)
    except Exception as e:
        print(f"⚠️ Generator Failed: {e}")
        # Fallback: Create simple extract shorts if AI fails
        shorts_data = [
            {"title": "Highlight 1", "script": script_text[:300] + "..."},
            {"title": "Highlight 2", "script": script_text[300:600] + "..."},
            {"title": "Highlight 3", "script": script_text[600:900] + "..."}
        ]

    # 4. Save to Files
    shorts_dir = os.path.join(target_folder, "shorts")
    os.makedirs(shorts_dir, exist_ok=True)

    for i, short in enumerate(shorts_data):
        file_path = os.path.join(shorts_dir, f"short_{i + 1}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(short, f, indent=4)
        print(f"   ✅ Created: short_{i + 1}.json")

    print("\n🎉 Repair Complete! Refresh your dashboard.")


if __name__ == "__main__":
    repair_shorts()