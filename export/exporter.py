# export/exporter.py

import os
import json
from datetime import date


def create_video_structure(
    topic,
    script_text,
    titles,
    description,
    tags,
    thumbnail_text,
    shorts_list,
    score_data,
    revenue_data,
    posting_time_data
):
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m_%b").upper()
    day = today.strftime("%Y-%m-%d")

    topic_slug = topic.lower().replace(" ", "-")[:40]

    base_path = f"uploads/{year}/{month}/{day}_{topic_slug}"

    long_path = f"{base_path}/long"
    shorts_path = f"{base_path}/shorts"
    meta_path = f"{base_path}/meta"

    os.makedirs(long_path, exist_ok=True)
    os.makedirs(shorts_path, exist_ok=True)
    os.makedirs(meta_path, exist_ok=True)

    # ---- LONG VIDEO FILES ----
    with open(f"{long_path}/01_script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)

    with open(f"{long_path}/02_titles.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(titles))

    with open(f"{long_path}/03_description.txt", "w", encoding="utf-8") as f:
        f.write(description)

    with open(f"{long_path}/04_tags.txt", "w", encoding="utf-8") as f:
        f.write(", ".join(tags))

    with open(f"{long_path}/05_thumbnail_text.txt", "w", encoding="utf-8") as f:
        f.write(thumbnail_text)

    # ---- SHORTS ----
    for i, short in enumerate(shorts_list, 1):
        with open(f"{shorts_path}/short_{i:02d}.txt", "w", encoding="utf-8") as f:
            f.write(short)

    # ---- META ----
    with open(f"{meta_path}/score.json", "w") as f:
        json.dump(score_data, f, indent=2)

    with open(f"{meta_path}/revenue_prediction.json", "w") as f:
        json.dump(revenue_data, f, indent=2)

    with open(f"{meta_path}/posting_time.json", "w") as f:
        json.dump(posting_time_data, f, indent=2)

    print(f"✅ Content saved at: {base_path}")
