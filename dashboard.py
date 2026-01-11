# dashboard.py
import streamlit as st
from pathlib import Path
from datetime import datetime
import json
import pandas as pd
import re

# ================= CONFIG ================= #
UPLOADS_DIR = Path("uploads")
DATA_DIR = Path("data")
STATE_FILE = UPLOADS_DIR / "_dashboard_state.json"
READY_DIR = Path("ready_to_upload")
READY_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="YouTube AI Creator Studio", page_icon="🎬", layout="wide")

# ================= STYLES ================= #
st.markdown("""
<style>
.card {background:#161b22;border-radius:14px;padding:16px;margin-bottom:16px;border:1px solid #30363d;}
.small {color:#8b949e;font-size:13px;}
.big {font-size:26px;font-weight:700;}
.badge {display:inline-block;padding:4px 10px;border-radius:10px;background:#238636;font-size:12px;margin-left:10px;}
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
    return sorted(UPLOADS_DIR.rglob("01_script.txt"), key=lambda p: p.stat().st_mtime, reverse=True)

def topic(p): return p.parent.parent.name
def read(p): return p.read_text(encoding="utf-8")
def meta(p):
    m = p.parent.parent / "meta" / "score.json"
    return json.loads(m.read_text()) if m.exists() else {}

def clean_11labs(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def script_feedback(text):
    notes = []
    if len(text.split("\n\n")[0].split()) > 60: notes.append("⚠️ Hook is too long.")
    if text.lower().count("subscribe") == 0: notes.append("➕ Add CTA.")
    return notes or ["✅ Script looks good."]

def weekly_data():
    for f in ["dashboard.csv", "performance_log.csv"]:
        path = DATA_DIR / f
        if path.exists():
            try:
                # FIX: Handle empty/bad CSVs so app doesn't crash
                df = pd.read_csv(path)
                if not df.empty and "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"])
                    return df
            except Exception:
                continue
    return None

def prep_upload(p, text):
    out = READY_DIR / topic(p)
    out.mkdir(exist_ok=True)
    (out / "script.txt").write_text(text)
    return out

# ================= SIDEBAR ================= #
st.sidebar.title("🎬 Creator Studio")
search = st.sidebar.text_input("🔍 Search")
items = [p for p in scripts() if search.lower() in read(p).lower() and not state.get(str(p), {}).get("archived")]

if not items:
    st.warning("No scripts found.")
    st.stop()

idx = st.sidebar.radio("📂 Scripts", range(len(items)), format_func=lambda i: topic(items[i]))
current = items[idx]
key = str(current)
state.setdefault(key, {})

# ================= MAIN ================= #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown(f"<div class='big'>{topic(current)}</div>", unsafe_allow_html=True)
m = meta(current)
st.markdown(f"<span class='badge'>{'US-CPM OPTIMIZED' if m.get('best_country') == 'USA' else 'GLOBAL'}</span>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("💰 Est Revenue", f"${m.get('revenue', '—')}")
c2.metric("📈 CPM", f"${m.get('cpm', '—')}")
c3.metric("🧠 Score", m.get("score", "—"))

text = read(current)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("✍️ Script")

# FIX: Added label_visibility="collapsed" to fix the warning
st.text_area("Script Content", text, height=420, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

a1, a2, a3 = st.columns(3)
with a1: st.download_button("🎙 ElevenLabs Clean", clean_11labs(text), file_name=f"{topic(current)}_11labs.txt")
with a2:
    if st.button("📤 Prepare Upload"):
        st.success(f"Ready at {prep_upload(current, text)}")
with a3:
    if st.button("🗑 Archive"):
        state[key]["archived"] = True
        save_state(state)
        st.rerun() # FIX: Updated from experimental_rerun