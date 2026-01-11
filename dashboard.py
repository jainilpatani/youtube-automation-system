# dashboard.py
import streamlit as st
from pathlib import Path
from datetime import datetime
import json
import pandas as pd
import re
import streamlit as st
import os

st.set_page_config(
    page_title="YouTube Automation Dashboard",
    layout="wide"
)

import shutil

# ================= CONFIG ================= #
UPLOADS_DIR = Path("uploads")
DATA_DIR = Path("data")
STATE_FILE = UPLOADS_DIR / "_dashboard_state.json"
READY_DIR = Path("ready_to_upload")
READY_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="YouTube AI Creator Studio",
    page_icon="🎬",
    layout="wide"
)

# ================= STYLES ================= #
st.markdown("""
<style>
.card {background:#161b22;border-radius:14px;padding:16px;margin-bottom:16px;border:1px solid #30363d;}
.small {color:#8b949e;font-size:13px;}
.big {font-size:26px;font-weight:700;}
.badge {display:inline-block;padding:4px 10px;border-radius:10px;background:#238636;font-size:12px;margin-left:10px;}
.warn {background:#9e6a03;}
</style>
""", unsafe_allow_html=True)

# ================= STATE ================= #
def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(s):
    STATE_FILE.write_text(json.dumps(s, indent=2))

state = load_state()

# ================= HELPERS ================= #
def scripts():
    return sorted(
        UPLOADS_DIR.rglob("01_script.txt"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

def topic(p): return p.parent.parent.name
def read(p): return p.read_text(encoding="utf-8")

def meta(p):
    m = p.parent.parent / "meta" / "score.json"
    return json.loads(m.read_text()) if m.exists() else {}

def clean_11labs(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[•*-]", "", text)
    return text.strip()

def script_feedback(text):
    notes = []
    if len(text.split("\n\n")[0].split()) > 60:
        notes.append("⚠️ Hook paragraph is long. Consider 1–2 shorter sentences.")
    if text.lower().count("subscribe") == 0:
        notes.append("➕ No CTA detected. Add one soft CTA near the end.")
    if max(len(p.split()) for p in text.split("\n\n")) > 120:
        notes.append("📉 Some paragraphs are long. Break them for better retention.")
    return notes or ["✅ Script structure looks good."]



def weekly_data():
    path = "data/performance_log.csv"

    # Case 1: File does not exist
    if not os.path.exists(path):
        return pd.DataFrame(columns=[
            "date",
            "topic",
            "views",
            "watch_time",
            "revenue"
        ])

    # Case 2: File exists but is empty or broken
    try:
        df = pd.read_csv(path)

        if df.empty:
            return pd.DataFrame(columns=[
                "date",
                "topic",
                "views",
                "watch_time",
                "revenue"
            ])

        return df

    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=[
            "date",
            "topic",
            "views",
            "watch_time",
            "revenue"
        ])

    except Exception:
        return pd.DataFrame(columns=[
            "date",
            "topic",
            "views",
            "watch_time",
            "revenue"
        ])

def prep_upload(p, text):
    out = READY_DIR / topic(p)
    out.mkdir(exist_ok=True)
    (out / "script.txt").write_text(text)
    (out / "description.txt").write_text(f"About this video:\n{topic(p)}")
    (out / "tags.txt").write_text(topic(p).replace(" ", ", "))
    (out / "thumbnail_text.txt").write_text(topic(p))
    return out

# ================= SIDEBAR ================= #
st.sidebar.title("🎬 Creator Studio")
search = st.sidebar.text_input("🔍 Search")

items = [
    p for p in scripts()
    if search.lower() in read(p).lower()
    and not state.get(str(p), {}).get("archived")
]

if not items:
    st.warning("No scripts found.")
    st.stop()

idx = st.sidebar.radio(
    "📂 Scripts",
    range(len(items)),
    format_func=lambda i: topic(items[i])
)

current = items[idx]
key = str(current)
state.setdefault(key, {})

# ================= MAIN ================= #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown(f"<div class='big'>{topic(current)}</div>", unsafe_allow_html=True)

m = meta(current)
badge = "US-CPM OPTIMIZED" if m.get("best_country") == "USA" else "GLOBAL"
st.markdown(f"<span class='badge'>{badge}</span>", unsafe_allow_html=True)

st.markdown(f"<div class='small'>Generated • {datetime.fromtimestamp(current.stat().st_mtime)}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Metrics
c1, c2, c3 = st.columns(3)
c1.metric("💰 Est Revenue (US)", f"${m.get('revenue', '—')}")
c2.metric("📈 CPM (US)", f"${m.get('cpm', '—')}")
c3.metric("🧠 Score", m.get("score", "—"))

# Script
text = read(current)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("✍️ Script")
st.text_area(
    label="Generated Script",
    value=text,
    height=420,
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

# Improvements
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🧠 Improvement Suggestions")
for n in script_feedback(text):
    st.write(n)
st.markdown("</div>", unsafe_allow_html=True)

# Actions
a1, a2, a3 = st.columns(3)
with a1:
    st.download_button("🎙 ElevenLabs Clean", clean_11labs(text), file_name=f"{topic(current)}_11labs.txt")
with a2:
    if st.button("📤 Prepare for Upload"):
        out = prep_upload(current, text)
        st.success(f"Ready at {out}")
with a3:
    if st.button("🗑 Archive"):
        state[key]["archived"] = True
        save_state(state)
        st.rerun()


# Weekly Graphs
df = weekly_data()
if df is not None:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Weekly Performance")
    # ---- SAFE DATE HANDLING ----
    if not df.empty and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

        if not df.empty:
            df_week = (
                df.set_index("date")
                .resample("W")
                .mean(numeric_only=True)
            )
        else:
            df_week = pd.DataFrame()
    else:
        df_week = pd.DataFrame()

    st.line_chart(df_week.select_dtypes("number"))
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Localhost • Creator-first • No APIs • Production workflow")
