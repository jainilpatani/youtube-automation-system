# main.py
from Core.trend_collector import get_google_trends, get_reddit_trends
from Core.topic_scorer import score_topics
from Core.analytics import create_dashboard
from Core.script_generator import generate_original_script
from Core.critic_writer import apply_critic_and_writer
from Core.shorts_generator import generate_shorts
from Core.memory_engine import load_memory, extract_patterns
from export.exporter import save_all

FALLBACK_TOPIC = "How AI is changing the future of work"


def run():
    print("🚀 Starting YouTube Automation System")

    # Collect trends
    google = get_google_trends()
    reddit = get_reddit_trends()

    # Score topics
    scored_topics = score_topics(google, reddit)

    # 🛑 Crash prevention
    if not scored_topics:
        print("⚠️ No topics found. Using fallback topic.")
        scored_topics = [(FALLBACK_TOPIC, 1)]

    dashboard = create_dashboard(scored_topics)
    print("\n📊 DASHBOARD PREVIEW")
    print(dashboard.head())

    best_topic, best_score = scored_topics[0]
    print(f"\n🏆 Selected Topic: {best_topic} (Score {best_score})")

    # Load memory
    memory = load_memory()
    style_notes_list = extract_patterns(memory)

    # ✅ Convert memory list → single string
    style_notes = "\n".join(style_notes_list) if style_notes_list else ""

    # Generate script
    draft_script = generate_original_script(best_topic)

    # Critic + Writer (JSON-safe)
    final_content = apply_critic_and_writer(
        draft_script=draft_script,
        style_notes=style_notes
    )

    # Generate Shorts
    shorts = generate_shorts(final_content["final_script"])

    # Save all outputs
    save_all(
        topic=best_topic,
        script=final_content,
        shorts=shorts
    )

    print("✅ Pipeline completed successfully")


if __name__ == "__main__":
    run()
