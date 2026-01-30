import sqlite3

DB_NAME = "automation.db"


def init_db():
    """Initializes the database with Money Columns."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # We create the table with cpm and revenue columns
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            viral_score INTEGER,
            cpm REAL DEFAULT 0.0,
            revenue REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Completed',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def add_video(topic, score, cpm, revenue):
    """Adds a new video entry with money stats."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO videos (topic, viral_score, cpm, revenue) VALUES (?, ?, ?, ?)',
              (topic, score, cpm, revenue))
    conn.commit()
    conn.close()


def get_all_videos():
    """Fetches all videos sorted by newest first."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM videos ORDER BY id DESC')
    return c.fetchall()


def get_stats():
    """Calculates dashboard totals."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get total count
    c.execute('SELECT COUNT(*) FROM videos')
    total_videos = c.fetchone()[0]

    # Get averages/totals
    c.execute('SELECT AVG(viral_score), SUM(revenue) FROM videos')
    row = c.fetchone()
    avg_score = round(row[0], 1) if row[0] else 0
    total_revenue = round(row[1], 2) if row[1] else 0.00

    conn.close()

    return {
        "total_videos": total_videos,
        "avg_score": avg_score,
        "est_revenue": total_revenue
    }
def delete_video(video_id):
    """Deletes a video record by ID."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM videos WHERE id = ?', (video_id,))
    conn.commit()
    conn.close()


# Initialize on import
init_db()