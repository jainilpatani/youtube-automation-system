# Core/trend_collector.py

from pytrends.request import TrendReq

def get_google_trends():
    """
    Safe Google Trends fetch.
    If Google blocks, fallback is used.
    """
    try:
        pytrends = TrendReq(hl="en-US", tz=330)
        trends_df = pytrends.trending_searches(pn="global")
        return trends_df[0].tolist()[:20]

    except Exception as e:
        print("⚠️ Google Trends blocked or unavailable. Using fallback trends.")
        return fallback_trends()


def fallback_trends():
    """
    High-CPM, YouTube-safe fallback topics
    (manually curated, stable)
    """
    return [
        "How AI is changing jobs",
        "AI tools businesses are using",
        "Future of work with AI",
        "How companies use artificial intelligence",
        "AI and the global economy",
        "Why AI is everywhere now",
        "How automation affects income",
        "Technology changing daily life",
        "AI explained simply",
        "How software is replacing manual work"
    ]


def get_reddit_trends():
    """
    Reddit is optional.
    If not configured, return empty list.
    """
    try:
        import praw
        from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

        if not REDDIT_CLIENT_ID:
            return []

        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        topics = []
        for post in reddit.subreddit("technology").hot(limit=10):
            topics.append(post.title)

        return topics

    except Exception:
        print("⚠️ Reddit unavailable. Skipping Reddit trends.")
        return []
