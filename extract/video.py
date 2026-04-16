import json
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build

def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname and 'youtube.com' in parsed.hostname:
        return parse_qs(parsed.query).get('v', [None])[0]
    elif parsed.hostname and 'youtu.be' in parsed.hostname:
        return parsed.path.lstrip('/')
    return None

def get_video_details(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )

    response = request.execute()

    if not response['items']:
        return None

    item = response['items'][0]['snippet']

    video_data = {
        "video_id": video_id,
        "title": item['title'],
        "channel_id": item['channelId'],
        "channel_name": item['channelTitle'],
        "published_at": item['publishedAt']
    }

    # 🔥 langsung save ke JSON di sini
    with open("data/raw/video.json", "w", encoding="utf-8") as f:
        json.dump(video_data, f, indent=4, ensure_ascii=False)

    return video_data