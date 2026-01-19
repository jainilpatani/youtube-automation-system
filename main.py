import sys
import os

# Ensure Core imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Core.trend_collector import get_google_trends, get_reddit_trends
from Core.topic_scorer import score_topics
from Core.analytics import create_dashboard
from Core.script_generator import generate_original_script
from Core.shorts_generator import generate_shorts
from Core.posting_time_ai import best_posting_time
from Core.memory_engine import load_memory, extract_patterns
from Core.critic_writer import apply_critic_and_writer
from export.exporter import save_all


def run():
    print("🚀 Starting SAFE YouTube Automation System\n")

    # 1. Trends
    print("📊 Collecting trends...")
    google_trends = get_google_trends()
    try:
        reddit_trends = get_reddit_trends()
    except:
        reddit_trends = []

    # 2. Score
    print("🧮 Scoring topics...")
    scored_topics = score_topics(google_trends, reddit_trends)
    if not scored_topics:
        scored_topics = [("AI Automation for Beginners", 85)]

    create_dashboard(scored_topics)
    best_topic, best_score = scored_topics[0]
    print(f"\n🏆 Selected TOPIC: {best_topic} (Score: {best_score})")

    # 3. Memory (POLISHED LOGIC)
    print("🧠 Loading channel memory...")
    memory = load_memory()
    patterns = extract_patterns(memory)

    # FIX: We extract the LIST from the DICT, then join it into a STRING
    style_notes_text = ""
    if patterns and "style_notes" in patterns:
        notes_list = patterns["style_notes"]
        if isinstance(notes_list, list):
            style_notes_text = " | ".join(map(str, notes_list[:5]))
            print(f"   ↳ Adapting to past wins: {style_notes_text[:60]}...")

    # 4. Generate & Critic
    print("\n✍️ Generating original draft...")
    draft_script = generate_original_script(best_topic)

    print("🧠 Applying critic + clarity writer...")
    # FIX: Pass the clean string, not the dictionary
    final_output = apply_critic_and_writer(
        draft_script=draft_script,
        style_notes=style_notes_text
    )

    if not final_output.get("script"):
        print("❌ Script generation failed.")
        return

    # 5. Shorts & Save
    print("📱 Generating Shorts...")
    try:
        shorts = generate_shorts(final_output["script"])
    except:
        shorts = []

    print("💾 Saving content...")
    save_all(topic=best_topic, script=final_output, shorts=shorts)

    print("\n✅ DONE")


if __name__ == "__main__":
    run()