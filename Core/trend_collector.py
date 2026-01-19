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
        print("⚠️ Google Trends blocked. Using B2B Fallback Trends.")
        return fallback_trends()


def fallback_trends():
    """
    B2B & Business Automation Trends (High CPM)
    Targeting business owners looking to cut costs/save time.
    """
    return [
        "Automating customer support with AI agents",
        "AI marketing workflows for small business",
        "Replacing middle management with software",
        "How to cut business costs using AI",
        "AI lead generation strategies 2025",
        "Automating payroll and HR systems",
        "The ROI of AI implementation",
        "Custom AI tools vs Enterprise software",
        "Scaling a business without hiring",
        "Future of B2B sales automation"
    ]


def get_reddit_trends():
    """
    Scans business-focused subreddits instead of generic tech.
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
        # CHANGED: Scans 'entrepreneur' and 'smallbusiness' for real pain points
        for sub in ["entrepreneur", "smallbusiness", "marketing"]:
            for post in reddit.subreddit(sub).hot(limit=3):
                topics.append(post.title)

        return topics

    except Exception:
        print("⚠️ Reddit unavailable. Skipping.")
        return []