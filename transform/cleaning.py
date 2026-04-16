import re

def clean_comments(comments):
    cleaned = []

    for c in comments:
        text = (c.get("text") or "").lower().strip()

        # hapus mention
        text = re.sub(r'@\w+', '', text)

        # hapus url
        text = re.sub(r'http\S+|www\S+', '', text)

        # hapus SEMUA selain huruf, angka, dan spasi
        text = re.sub(r'[^a-z0-9\s]', '', text)

        # rapihin spasi
        text = re.sub(r'\s+', ' ', text).strip()

        cleaned.append({
            "comment_id": c.get("comment_id"),
            "author_id": c.get("author_id"),
            "author_name": (c.get("author_name") or "").lower().strip(),
            "text": text,
            "like_count": c.get("like_count", 0),
            "published_at": c.get("published_at")
        })

    return cleaned