import json
import psycopg2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG

def load_to_db():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "data", "processed", "warehouse.json")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # =========================
        # DIM CHANNEL
        # =========================
        for row in data["dim_channel"]:
            cur.execute("""
                INSERT INTO dim_channel (channel_id, channel_name)
                VALUES (%s, %s)
                ON CONFLICT (channel_id) DO NOTHING
            """, (row["channel_id"], row["channel_name"]))

        # =========================
        # DIM VIDEO
        # =========================
        for row in data["dim_video"]:
            cur.execute("""
                INSERT INTO dim_video (video_id, title, channel_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (video_id) DO NOTHING
            """, (row["video_id"], row["title"], row["channel_id"]))

        # =========================
        # DIM AUTHOR
        # =========================
        for row in data["dim_author"]:
            cur.execute("""
                INSERT INTO dim_author (author_id, author_name)
                VALUES (%s, %s)
                ON CONFLICT (author_id) DO NOTHING
            """, (row["author_id"], row["author_name"]))

        # =========================
        # DIM DATE
        # =========================
        for row in data["dim_date"]:
            cur.execute("""
                INSERT INTO dim_date (date_id, date)
                VALUES (%s, %s)
                ON CONFLICT (date_id) DO NOTHING
            """, (row["date_id"], row["date"]))

        # =========================
        # FACT COMMENTS
        # =========================
        for row in data["fact_comments"]:
            cur.execute("""
                INSERT INTO fact_comments 
                (comment_id, video_id, author_id, date_id, comment_text, like_count)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (comment_id) DO NOTHING
            """, (
                row["comment_id"],
                row["video_id"],
                row["author_id"],
                row["date_id"],
                row["text"],
                row["like_count"]
            ))

        conn.commit()
        print("✅ Data berhasil di-load ke PostgreSQL!")

    except Exception as e:
        import traceback
        print(traceback.format_exc())

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# if __name__ == "__main__":
#     print("🚀 Start loading to PostgreSQL...")
#     load_to_db()
