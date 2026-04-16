import streamlit as st
import pandas as pd
import json
import os

from config import API_KEY
from extract.video import get_video_id, get_video_details
from extract.comments import extract_comments
from transform.transform import run_transform
from load.load_to_postgres import load_to_db

st.title("YouTube Comment Scraper")

url = st.text_input("Paste link YouTube:")

if st.button("Scrape") and url:

    video_id = get_video_id(url)

    if video_id:
        with st.spinner("🚀 Processing... (Extract + Transform)"):
            
            # 🔥 EXTRACT
            get_video_details(video_id, API_KEY)
            extract_comments(video_id, API_KEY)

            # 🔥 TRANSFORM
            run_transform()
            st.success("✅ Data berhasil diproses!")
            
            load_to_db()
            


        # 🔥 LOAD HASIL WAREHOUSE
        path = "data/processed/warehouse.json"

        if not os.path.exists(path):
            st.error("❌ Warehouse tidak ditemukan!")
            st.stop()

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # =========================
        # 📊 DASHBOARD
        # =========================
        st.subheader("Summary")
        st.write("Jumlah komentar:", len(data["fact_comments"]))
        st.write("Jumlah author:", len(data["dim_author"]))
        st.write("Jumlah tanggal:", len(data["dim_date"]))

        # =========================
        # 💾 Download Excel (langsung dari file)
        # =========================
        excel_path = "data/raw/comments.xlsx"

        if os.path.exists(excel_path):
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="📥 Download data komentar mentah",
                    data=f,
                    file_name="youtube_comments.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("⚠️ File Excel komentar belum tersedia")
        # Tabs
        tabs = st.tabs([
            "Fact Comments",
            "Dim Video",
            "Dim Channel",
            "Dim Author",
            "Dim Date"
        ])

        keys = ["fact_comments","dim_video","dim_channel","dim_author","dim_date"]

        for tab, key in zip(tabs, keys):
            with tab:
                st.dataframe(pd.DataFrame(data[key]))

    else:
        st.error("❌ Link tidak valid")
