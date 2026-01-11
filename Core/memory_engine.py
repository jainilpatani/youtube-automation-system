import pandas as pd

def load_memory():
    try:
        return pd.read_csv("channel_memory.csv")
    except:
        return None

def extract_patterns(df):
    if df is None:
        return {}

    winners = df[df["views"] > 50000]
    return {
        "best_topics": winners["topic"].tolist(),
        "style_notes": winners["style_notes"].tolist()
    }
