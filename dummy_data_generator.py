import shutil
import json
import random
from pathlib import Path

# ================= CONFIG ================= #
UPLOADS_DIR = Path("uploads")

# Dummy Topics to simulate
TOPICS = [
    "Why AI Agents Will Replace Middle Management",
    "Python vs Rust for 2025 - The Brutal Truth",
    "7 Passive Income Streams That Actually Work",
    "How to Automate Your Life with Zapier",
    "The Collapse of the Junior Developer Market"
]

# ================= CONTENT TEMPLATES ================= #
DUMMY_SCRIPT_TEMPLATE = """
**Title:** {topic}

**Hook:**
Stop scrolling. You have been lied to about {keyword}. The old way is dead, and if you don't adapt, you will be left behind. In the next 5 minutes, I'm going to show you exactly why.

**Intro:**
Welcome back to the channel. Today we are breaking down {topic}. I've spent 50 hours analyzing the data so you don't have to.

**Point 1: The Problem**
Most people think they are safe. They aren't. Data shows that 40% of jobs in this sector are at risk.

**Point 2: The Solution**
Here is the fix. You need to start building leverage.

**Conclusion:**
Don't wait until it's too late. Start today.

**CTA:**
If you found value in this, hit subscribe. It helps the channel grow.
"""


def clean_uploads():
    """Wipes the uploads folder to start fresh."""
    if UPLOADS_DIR.exists():
        shutil.rmtree(UPLOADS_DIR)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    print("🧹 Cleaned 'uploads' directory.")


def generate_dummy_data():
    clean_uploads()

    print("🛠️ Generating dummy data...")

    for topic in TOPICS:
        # 1. Create Folder Structure
        # Matches dashboard.py logic: uploads/{topic}/content/01_script.txt
        safe_name = topic.replace(" ", "_").replace("-", "_")
        topic_dir = UPLOADS_DIR / safe_name

        meta_dir = topic_dir / "meta"
        content_dir = topic_dir / "content"  # Assuming script sits here based on dashboard logic

        meta_dir.mkdir(parents=True, exist_ok=True)
        content_dir.mkdir(parents=True, exist_ok=True)

        # 2. Generate Meta Data (score.json)
        score_data = {
            "topic": topic,
            "score": random.randint(75, 98),
            "best_country": random.choice(["USA", "UK", "Canada", "India"]),
            "cpm": round(random.uniform(12.5, 35.0), 2),
            "revenue": round(random.uniform(150.0, 5000.0), 2)
        }
        (meta_dir / "score.json").write_text(json.dumps(score_data, indent=2))

        # 3. Generate Script (01_script.txt)
        keyword = topic.split()[-1]
        script_content = DUMMY_SCRIPT_TEMPLATE.format(topic=topic, keyword=keyword)
        (content_dir / "01_script.txt").write_text(script_content, encoding="utf-8")

        print(f"   ✅ Created: {topic}")

    print("\n🎉 Done! Run 'streamlit run dashboard.py' to see the data.")


if __name__ == "__main__":
    generate_dummy_data()