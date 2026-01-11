import streamlit as st
from pathlib import Path
from datetime import datetime
import json
import pandas as pd
import re

# CONFIG
UPLOADS_DIR = Path("uploads")
DATA_DIR = Path("data")
STATE_FILE = UPLOADS_DIR / "_dashboard_state.json"
READY_DIR = Path("ready_to_upload")
READY_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="YouTube AI Studio", page_icon="🎬", layout="wide")

# STYLES
st.markdown("""
<style>
.card {background:#161b22;border-radius:14px;padding:16px;margin-bottom:16px;border:1px solid #30363d;}
.big {font-size:26px;font-weight:700;}
.badge {display:inline-block;padding:4px 10px;border-radius:10px;background:#238636;font-size:12px;margin-left:10px;}
</style>
""", unsafe_allow_html=True)

# HELPERS
def load_state():
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}

def save_state(s):
    STATE_FILE.write_text(json.dumps(s, indent=2))

state = load_state()

def scripts():
    return sorted(UPLOADS_DIR.rglob("01_script.txt"), key=lambda p: p.stat().st_mtime, reverse=True)

def topic(p): return p.parent.parent.name
def read(p): return p.read_text(encoding="utf-8")
def meta(p):
    m = p.parent.parent / "meta" / "score.json"
    return json.loads(m.read_text()) if m.exists() else {}

def weekly_data():
    """Safely loads CSV without crashing on empty files"""
    for f in ["dashboard.csv", "performance_log.csv"]:
        path = DATA_DIR / f
        if path.exists():
            try:
                df = pd.read_csv(path)
                if not df.empty and "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"])
                    return df
            except: continue
    return None

def prep_upload(p, text):
    out = READY_DIR / topic(p)
    out.mkdir(exist_ok=True)
    (out / "script.txt").write_text(text)
    return out

# UI
st.sidebar.title("🎬 AI Studio")
items = [p for p in scripts() if not state.get(str(p), {}).get("archived")]

if not items:
    st.warning("No scripts found. Run main.py first!")
    st.stop()

idx = st.sidebar.radio("Select Script", range(len(items)), format_func=lambda i: topic(items[i]))
current = items[idx]
m = meta(current)

st.markdown(f"<div class='card'><div class='big'>{topic(current)}</div></div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("💰 Revenue", f"${m.get('revenue', '—')}")
c2.metric("📈 CPM", f"${m.get('cpm', '—')}")
c3.metric("🧠 Score", m.get("score", "—"))

text = read(current)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("✍️ Script Content")
# FIX: Added label_visibility="collapsed" to silence the warning
st.text_area("Script", text, height=420, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
if c1.button("📤 Prepare Upload"):
    path = prep_upload(current, text)
    st.success(f"Saved to {path}")
if c2.button("🗑 Archive"):
    state[str(current)] = {"archived": True}
    save_state(state)
    st.rerun()

df = weekly_data()
if df is not None:
    st.line_chart(df.set_index("date").resample("W").mean(numeric_only=True))