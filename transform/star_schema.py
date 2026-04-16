def build_star_schema(comments, video_data):

    video_id = video_data.get("video_id") or "unknown_video"
    channel_id = video_data.get("channel_id") or "unknown_channel"

    # --- DIM VIDEO ---
    dim_video = {
        video_id: {
            "video_id": video_id,
            "title": (video_data.get("title") or "").lower().strip(),
            "channel_id": channel_id,
            "published_at": video_data.get("published_at")
        }
    }

    # --- DIM CHANNEL ---
    dim_channel = {
        channel_id: {
            "channel_id": channel_id,
            "channel_name": (video_data.get("channel_name") or "").lower().strip()
        }
    }

    dim_author = {}
    dim_date = {}
    fact_comments = []

    seen_comments = set()

    for c in comments:
        comment_id = c.get("comment_id")
        published_at = c.get("published_at")
        text = (c.get("text") or "").strip()

        # ❌ skip data rusak
        if not comment_id or not published_at or not text:
            continue

        # ❌ deduplicate
        if comment_id in seen_comments:
            continue
        seen_comments.add(comment_id)

        author_id = c.get("author_id") or "unknown_author"

        # 🔥 SAFE DATE HANDLING
        try:
            date = published_at[:10]  # YYYY-MM-DD
            date_id = date.replace("-", "")
            year = date[:4]
            month = date[5:7]
            day = date[8:10]
        except:
            continue  # skip kalau format aneh

        # --- DIM AUTHOR ---
        if author_id not in dim_author:
            dim_author[author_id] = {
                "author_id": author_id,
                "author_name": (c.get("author_name") or "unknown").strip()
            }

        # --- DIM DATE ---
        if date_id not in dim_date:
            dim_date[date_id] = {
                "date_id": date_id,
                "date": date,
                "year": int(year),
                "month": int(month),
                "day": int(day)
            }

        # --- FACT ---
        fact_comments.append({
            "comment_id": comment_id,
            "video_id": video_id,
            "channel_id": channel_id,
            "author_id": author_id,
            "date_id": date_id,
            "like_count": int(c.get("like_count") or 0),
            "text": text
        })

    return {
        "dim_video": list(dim_video.values()),
        "dim_channel": list(dim_channel.values()),
        "dim_author": list(dim_author.values()),
        "dim_date": list(dim_date.values()),
        "fact_comments": fact_comments
    }