import json
import psycopg2
import os
import streamlit as st
from config import DB_CONFIG

def load_to_db():
    conn = None
    cur = None

    try:
        st.write("🚀 START LOAD DB")

        # CONNECT DB
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        st.write("✅ CONNECTED TO DB")

        # CHECK DB INFO
        cur.execute("SELECT current_database(), current_user;")
        st.write("DB INFO:", cur.fetchone())

        # FILE PATH
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "data", "processed", "warehouse.json")

        st.write("📂 FILE PATH:", file_path)
        st.write("FILE EXISTS:", os.path.exists(file_path))

        # LOAD JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        st.write("📊 DATA COUNT:")
        st.write("dim_channel:", len(data["dim_channel"]))
        st.write("dim_video:", len(data["dim_video"]))
        st.write("dim_author:", len(data["dim_author"]))
        st.write("dim_date:", len(data["dim_date"]))
        st.write("fact_comments:", len(data["fact_comments"]))

        # =========================
        # DIM CHANNEL
        # =========================
        for row in data["dim_channel"]:
            cur.execute("""
                INSERT INTO dim_channel (channel_id, channel_name)
                VALUES (%s, %s)
                ON CONFLICT (channel_id) DO NOTHING
            """, (row["channel_id"], row["channel_name"]))

        st.write("✅ DIM CHANNEL DONE")

        # =========================
        # DIM VIDEO
        # =========================
        for row in data["dim_video"]:
            cur.execute("""
                INSERT INTO dim_video (video_id, title, channel_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (video_id) DO NOTHING
            """, (row["video_id"], row["title"], row["channel_id"]))

        st.write("✅ DIM VIDEO DONE")

        # =========================
        # DIM AUTHOR
        # =========================
        for row in data["dim_author"]:
            cur.execute("""
                INSERT INTO dim_author (author_id, author_name)
                VALUES (%s, %s)
                ON CONFLICT (author_id) DO NOTHING
            """, (row["author_id"], row["author_name"]))

        st.write("✅ DIM AUTHOR DONE")

        # =========================
        # DIM DATE
        # =========================
        for row in data["dim_date"]:
            cur.execute("""
                INSERT INTO dim_date (date_id, date)
                VALUES (%s, %s)
                ON CONFLICT (date_id) DO NOTHING
            """, (row["date_id"], row["date"]))

        st.write("✅ DIM DATE DONE")

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

        st.write("✅ FACT COMMENTS DONE")

        # COMMIT
        conn.commit()
        st.success("🎉 DATA BERHASIL MASUK DB!")

    except Exception as e:
        import traceback
        st.error("❌ ERROR SAAT LOAD DB")
        st.text(traceback.format_exc())

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
