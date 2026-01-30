import requests
import xml.etree.ElementTree as ET

# 📡 CONFIG: Sources
GOOGLE_QUERY = "AI Automation Business OR SaaS OR AI Agents"
GOOGLE_RSS = f"https://news.google.com/rss/search?q={GOOGLE_QUERY}+when:7d&hl=en-US&gl=US&ceid=US:en"

# 👽 REDDIT CONFIG (No Keys Needed)
# We look at specific subreddits for "Top" posts of the day
REDDIT_SUBS = [
    "https://www.reddit.com/r/ArtificialInteligence/top/.rss?t=day",
    "https://www.reddit.com/r/ChatGPT/top/.rss?t=day",
    "https://www.reddit.com/r/SaaS/top/.rss?t=day"
]


def get_google_trends():
    """Fetches LIVE news from Google RSS."""
    print(f"📡 Connecting to Google News ({GOOGLE_QUERY})...")
    trends = []

    try:
        response = requests.get(GOOGLE_RSS, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('./channel/item')[:3]:
                title = item.find('title').text.rsplit(' - ', 1)[0]
                trends.append({"title": title, "traffic": "🔥 Google News", "source": "Google"})
    except Exception as e:
        print(f"⚠️ Google RSS Failed: {e}")

    return trends


def get_reddit_trends():
    """Fetches Reddit Data via Public RSS (Bypasses API Key requirement)."""
    print("👽 Connecting to Reddit Public Feeds...")
    trends = []

    # We must pretend to be a real browser to avoid blocks
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for url in REDDIT_SUBS:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                # Get the #1 top post from each subreddit
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry')[:1]:
                    title = entry.find('{http://www.w3.org/2005/Atom}title').text
                    link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
                    subreddit = url.split('/r/')[1].split('/')[0]

                    trends.append({
                        "title": title,
                        "traffic": f"✨ r/{subreddit}",
                        "source": "Reddit"
                    })
        except Exception:
            continue  # If one fails, try the next

    if not trends:
        print("⚠️ Reddit RSS blocked (IP restriction). Skipping Reddit.")

    return trends