def predict_watch_time(score, video_length):
    retention = min(0.35 + score * 0.015, 0.72)
    avd = retention * video_length

    return {
        "retention_percent": round(retention * 100, 2),
        "avg_view_duration": round(avd, 1),
        "rewatch": "High" if retention > 0.55 else "Medium"
    }
