from flask import Flask, render_template, request, redirect, url_for, abort
import pandas as pd
import os
import subprocess
import ast
import json
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "dashboard.csv"
UPLOADS_DIR = "uploads"


# --- HELPER: Turn Robot Text into Human HTML ---
def format_script_to_html(raw_text):
    """Parses raw script text into HTML cards."""
    html_output = ""
    raw_text = raw_text.strip()
    try:
        parsed_data = ast.literal_eval(raw_text)
        if isinstance(parsed_data, dict):
            if 'timestamp' in parsed_data:
                parsed_data = [parsed_data]
            else:
                parsed_data = [{'timestamp': k, **v} for k, v in parsed_data.items()]

        if isinstance(parsed_data, list):
            for scene in parsed_data:
                time = scene.get('timestamp', 'Scene')
                details = scene.get('scene', scene)
                visual = details.get('visual', scene.get('visual', ''))
                audio = details.get('host', scene.get('host', ''))

                html_output += f"""
                <div class="scene-card">
                    <div class="time-badge">⏰ {time}</div>
                    <div class="content-grid">
                        <div class="col-visual"><span class="icon">👀</span> <strong>VISUAL:</strong><br>{visual}</div>
                        <div class="col-audio"><span class="icon">🎙️</span> <strong>AUDIO:</strong><br>{audio}</div>
                    </div>
                </div>"""
            return html_output
    except:
        pass
    return f"<div class='plain-text'>{raw_text}</div>"


def get_stats():
    """Reads CSV and returns dashboard stats."""
    if not os.path.exists(CSV_FILE): return [], 0, "N/A", "Unknown"
    try:
        df = pd.read_csv(CSV_FILE)
        df.columns = [c.lower() for c in df.columns]
        if 'date' not in df.columns: df['date'] = datetime.now().strftime("%Y-%m-%d")
        if 'date' in df.columns: df = df.sort_values(by='date', ascending=False)
        return df.to_dict(orient='records'), len(df), int(
            df['score'].mean()) if 'score' in df.columns else 0, datetime.fromtimestamp(
            os.path.getmtime(CSV_FILE)).strftime("%B %d, %H:%M")
    except:
        return [], 0, 0, "Error"


def get_video_details(topic):
    """Finds ALL files (Script, Tags, Titles, Meta) for a topic."""
    slug = topic.lower().replace(" ", "-")[:40]

    video_data = {
        "script_html": "<p>No script found.</p>",
        "titles": "N/A",
        "tags": "N/A",
        "thumbnail": "N/A",
        "score": {},
        "revenue": {}
    }

    for root, dirs, files in os.walk(UPLOADS_DIR):
        if root.endswith(slug):
            # 1. Script
            script_path = os.path.join(root, "long", "01_script.txt")
            if os.path.exists(script_path):
                with open(script_path, "r", encoding="utf-8") as f:
                    video_data["script_html"] = format_script_to_html(f.read())

            # 2. Titles
            title_path = os.path.join(root, "long", "02_titles.txt")
            if os.path.exists(title_path):
                with open(title_path, "r", encoding="utf-8") as f:
                    video_data["titles"] = f.read()

            # 3. Tags
            tags_path = os.path.join(root, "long", "04_tags.txt")
            if os.path.exists(tags_path):
                with open(tags_path, "r", encoding="utf-8") as f:
                    video_data["tags"] = f.read()

            # 4. Thumbnail
            thumb_path = os.path.join(root, "long", "05_thumbnail_text.txt")
            if os.path.exists(thumb_path):
                with open(thumb_path, "r", encoding="utf-8") as f:
                    video_data["thumbnail"] = f.read()

            # 5. Meta (Score & Revenue)
            meta_path = os.path.join(root, "meta", "score.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    video_data["score"] = json.load(f)

            return video_data

    return None


@app.route('/')
def dashboard():
    data, total, score, updated = get_stats()
    return render_template('index.html', videos=data, total_videos=total, avg_score=score, last_updated=updated)


@app.route('/run-bot', methods=['POST'])
def run_bot():
    try:
        subprocess.Popen(["python", "main.py"])
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error: {e}"


@app.route('/view/<path:topic>')
def view_script(topic):
    details = get_video_details(topic)
    if details:
        return render_template('script_view.html', topic=topic, **details)
    else:
        return f"<h3>Files not found for: {topic}</h3><a href='/'>Go Back</a>"


if __name__ == '__main__':
    app.run(debug=True, port=5000)