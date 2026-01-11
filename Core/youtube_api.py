# Core/youtube_api.py
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY


def get_competitor_analysis(topic: str) -> str:
    """
    Fetches real-time viral video data for a specific topic.
    Returns a text summary for the AI writer.
    """
    if not YOUTUBE_API_KEY or "YOUR_" in YOUTUBE_API_KEY:
        return "No YouTube API Key provided. Skipping competitor analysis."

    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        # 1. Search for top videos
        search_response = youtube.search().list(
            q=topic,
            part="id,snippet",
            maxResults=5,
            type="video",
            order="relevance"
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_response['items']]
        if not video_ids:
            return "No competitor videos found."

        # 2. Get Video Stats (Views)
        stats_response = youtube.videos().list(
            id=",".join(video_ids),
            part="statistics,snippet"
        ).execute()

        # 3. Get Channel Stats (Subscribers) to find "Outliers"
        channel_ids = [item['snippet']['channelId'] for item in stats_response['items']]
        channels_response = youtube.channels().list(
            id=",".join(set(channel_ids)),
            part="statistics"
        ).execute()

        # Map channel ID to subscriber count
        channel_subs = {
            item['id']: int(item['statistics']['subscriberCount'])
            for item in channels_response['items']
            if not item['statistics']['hiddenSubscriberCount']
        }

        # 4. Analyze Data
        analysis = []
        for item in stats_response['items']:
            title = item['snippet']['title']
            views = int(item['statistics'].get('viewCount', 0))
            channel_id = item['snippet']['channelId']
            subs = channel_subs.get(channel_id, 1)  # avoid divide by zero

            # Viral Ratio: How many times more views than subscribers?
            ratio = round(views / subs, 1)
            is_outlier = ratio > 2.0  # If views are 2x subscribers, it's a content win

            note = f"- '{title}' ({views:,} views)"
            if is_outlier:
                note += f" 🔥 OUTLIER (Views are {ratio}x higher than subs!)"
            analysis.append(note)

        return "TOP COMPETITOR VIDEOS:\n" + "\n".join(analysis)

    except Exception as e:
        return f"Error fetching competitor data: {str(e)}"