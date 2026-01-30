import os
import json
import ast
from datetime import date


def format_script_for_human(content):
    if isinstance(content, str) and content.strip().startswith("{"):
        try:
            content = json.loads(content)
        except:
            pass

    if isinstance(content, dict):
        readable = "# 🎬 VIDEO SCRIPT\n\n"
        for time, dets in content.items():
            if isinstance(dets, dict):
                readable += f"### ⏰ {time}\n**👀 VISUAL:** {dets.get('visual', '')}\n**🎙️ AUDIO:** {dets.get('host', '')}\n\n"
        return readable

    if isinstance(content, list): return "\n\n".join(str(x) for x in content)
    return str(content)


def create_video_structure(topic, script_text, titles, description, tags, thumbnail_text, shorts_list, score_data,
                           revenue_data, posting_time_data):
    today = date.today()
    base_path = f"uploads/{today.strftime('%Y')}/{today.strftime('%m_%b').upper()}/{today.strftime('%Y-%m-%d')}_{topic.lower().replace(' ', '-')[:40]}"

    for d in ["long", "shorts", "meta"]: os.makedirs(f"{base_path}/{d}", exist_ok=True)

    with open(f"{base_path}/long/01_script.txt", "w", encoding="utf-8") as f:
        f.write(format_script_for_human(script_text))
    with open(f"{base_path}/long/02_titles.txt", "w", encoding="utf-8") as f:
        f.write(str(titles))
    with open(f"{base_path}/long/03_description.txt", "w", encoding="utf-8") as f:
        f.write(str(description))
    with open(f"{base_path}/long/04_tags.txt", "w", encoding="utf-8") as f:
        f.write(str(tags))
    with open(f"{base_path}/long/05_thumbnail_text.txt", "w", encoding="utf-8") as f:
        f.write(str(thumbnail_text))

    if shorts_list:
        for i, s in enumerate(shorts_list, 1):
            with open(f"{base_path}/shorts/short_{i:02d}.txt", "w", encoding="utf-8") as f:
                f.write(json.dumps(s, indent=2) if isinstance(s, dict) else str(s))

    with open(f"{base_path}/meta/score.json", "w") as f:
        json.dump(score_data, f, indent=2)
    print(f"✅ Content saved at: {base_path}")


def save_all(topic, script, shorts, score=0, posting_time="N/A"):
    """
    Accepts 'score' and 'posting_time' to generate real predictions.
    """
    # 1. Extract Data
    script_body = script.get("script", "")
    title = script.get("title", f"Video about {topic}")
    thumbnail = script.get("thumbnail", "Impactful Visual")
    keywords = script.get("keywords", [])

    # 2. Calculate Revenue (Est. $25.00 RPM for B2B niche)
    views_est = score * 1000
    revenue_est = round((views_est / 1000) * 25.00, 2)

    # 3. Save
    create_video_structure(
        topic=topic,
        script_text=script_body,
        titles=title,
        description=f"Video about {topic}.\n\nTags: {', '.join(keywords)}",
        tags=keywords,
        thumbnail_text=thumbnail,
        shorts_list=shorts,
        score_data={
            "score": score,
            "cpm": "25.00",
            "revenue": revenue_est,
            "best_country": "USA",
            "best_posting_time": posting_time  # <--- NEW FIELD ADDED
        },
        revenue_data={"est_revenue": revenue_est},
        posting_time_data={"status": "To be scheduled"}
    )