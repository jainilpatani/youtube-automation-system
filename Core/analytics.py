import pandas as pd
from Core.cpm_optimizer import best_countries
from Core.watchtime_predictor import predict_watch_time

from config import VIDEO_LENGTH_SECONDS

def create_dashboard(scored_topics):
    rows = []
    countries = best_countries()
    best_country = max(countries, key=countries.get)
    cpm = countries[best_country]

    for topic, score in scored_topics:
        views = min(score * 1200, 500_000)
        revenue = round((views / 1000) * cpm, 2)
        watch = predict_watch_time(score, VIDEO_LENGTH_SECONDS)

        rows.append({
            "Topic": topic,
            "Score": score,
            "Est Views": views,
            "Est Revenue ($)": revenue,
            "Best Country": best_country,
            "CPM": cpm,
            "Retention %": watch["retention_percent"],
            "Avg View Duration (sec)": watch["avg_view_duration"]
        })

    df = pd.DataFrame(rows)
    df.to_csv("dashboard.csv", index=False)
    return df
