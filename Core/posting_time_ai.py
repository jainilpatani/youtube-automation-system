import pandas as pd

def best_posting_time():
    df = pd.read_csv("posting_data.csv")
    best = df.sort_values("views", ascending=False).iloc[0]

    return f"Post on {best['day']} at {best['hour']}:00"
