# --------------- Versi 1 ----------------

def versi_1():
    import json
    from googleapiclient.discovery import build

    def extract_comments(video_id, api_key):
        youtube = build('youtube', 'v3', developerKey=api_key)

        comments = []
        next_page_token = None

        while True:
            request = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat='plainText'
            )

            response = request.execute()

            for thread in response['items']:

                # --- top-level ---
                top = thread['snippet']['topLevelComment']['snippet']
                comments.append({
                    "comment_id": thread['snippet']['topLevelComment']['id'],
                    "author_id": top.get('authorChannelId', {}).get('value'),
                    "author_name": top.get('authorDisplayName'),
                    "text": top.get('textDisplay'),
                    "like_count": top.get('likeCount', 0),
                    "published_at": top.get('publishedAt')
                })

                # --- replies ---
                if 'replies' in thread:
                    for reply in thread['replies']['comments']:
                        r = reply['snippet']
                        comments.append({
                            "comment_id": reply['id'],
                            "author_id": r.get('authorChannelId', {}).get('value'),
                            "author_name": r.get('authorDisplayName'),
                            "text": r.get('textDisplay'),
                            "like_count": r.get('likeCount', 0),
                            "published_at": r.get('publishedAt')
                        })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        # 🔥 save ke JSON langsung di sini
        with open("data/raw/comments.json", "w", encoding="utf-8") as f:
            json.dump(comments, f, indent=4, ensure_ascii=False)

        return comments



# --------------- Versi 2 ----------------

import json
import pandas as pd
from googleapiclient.discovery import build
import os

def extract_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat='plainText'
        )

        response = request.execute()

        for thread in response['items']:

            # --- top-level ---
            top = thread['snippet']['topLevelComment']['snippet']
            comments.append({
                "comment_id": thread['snippet']['topLevelComment']['id'],
                "author_id": top.get('authorChannelId', {}).get('value'),
                "author_name": top.get('authorDisplayName'),
                "text": top.get('textDisplay'),
                "like_count": top.get('likeCount', 0),
                "published_at": top.get('publishedAt')
            })

            # --- replies ---
            if 'replies' in thread:
                for reply in thread['replies']['comments']:
                    r = reply['snippet']
                    comments.append({
                        "comment_id": reply['id'],
                        "author_id": r.get('authorChannelId', {}).get('value'),
                        "author_name": r.get('authorDisplayName'),
                        "text": r.get('textDisplay'),
                        "like_count": r.get('likeCount', 0),
                        "published_at": r.get('publishedAt')
                    })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    # =========================
    # 📁 Setup folder
    # =========================
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # =========================
    # 💾 Save JSON (RAW)
    # =========================
    json_path = "data/raw/comments.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(comments, f, indent=4, ensure_ascii=False)

    # =========================
    # 📊 Convert ke DataFrame
    # =========================
    df = pd.DataFrame(comments)

    # (optional) rapihin kolom
    df = df[[
        "comment_id",
        "author_id",
        "author_name",
        "text",
        "like_count",
        "published_at"
    ]]

    # =========================
    # 💾 Save Excel (PROCESSED)
    # =========================
    excel_path = "data/raw/comments.xlsx"
    df.to_excel(excel_path, index=False)

    print(f"✅ JSON saved at: {json_path}")
    print(f"✅ Excel saved at: {excel_path}")

    return comments, df