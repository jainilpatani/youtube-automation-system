import pandas as pd
import random
import os
from datetime import datetime

DATA_FILE = "posting_data.csv"


def best_posting_time():
    """
    Analyzes past video performance to suggest the best upload time.
    If no data exists, it provides a 'Cold Start' suggestion based on B2B best practices.
    """

    # 1. Check if data exists. If not, return default advice.
    if not os.path.exists(DATA_FILE):
        print(f"⚠️ {DATA_FILE} not found. Using default B2B strategy.")
        return "Tuesday at 10:00 AM (EST)"

    try:
        df = pd.read_csv(DATA_FILE)

        # If dataset is too small, stick to defaults
        if len(df) < 5:
            return "Tuesday at 10:00 AM (EST) (Need more data)"

        # Simple Logic: Find the hour with the highest average score
        # (In a real scenario, you would track Views/Revenue here)
        if 'Score' in df.columns and 'Hour' in df.columns:
            best_hour = df.groupby('Hour')['Score'].mean().idxmax()
            return f"Best calculated time: {int(best_hour)}:00 (Based on {len(df)} videos)"

    except Exception as e:
        print(f"⚠️ Error reading posting data: {e}")

    # Fallback
    return "Wednesday at 11:00 AM (EST)"


# Helper to simulate saving data (for when you actually upload)
def record_performance(day, hour, score):
    new_data = pd.DataFrame([[day, hour, score]], columns=['Day', 'Hour', 'Score'])
    if not os.path.exists(DATA_FILE):
        new_data.to_csv(DATA_FILE, index=False)
    else:
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)