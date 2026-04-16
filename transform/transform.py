import json
import os
from .cleaning import clean_comments
from .star_schema import build_star_schema

# 🔥 ambil root project (1 level dari transform/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json(path):
    if not os.path.exists(path):
        print(f"❌ File tidak ditemukan: {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def run_transform():
    print("🚀 Start Transform...")

    comments_path = os.path.join(BASE_DIR, "data/raw/comments.json")
    video_path = os.path.join(BASE_DIR, "data/raw/video.json")

    comments = load_json(comments_path)
    video_data = load_json(video_path)

    if not comments:
        print("❌ No comments found!")
        return

    if not video_data:
        print("❌ No video data found!")
        return

    print(f"✅ Raw comments: {len(comments)}")

    comments_clean = clean_comments(comments)
    print(f"🧹 Clean comments: {len(comments_clean)}")

    warehouse = build_star_schema(comments_clean, video_data)
    print(f"🧱 Fact rows: {len(warehouse['fact_comments'])}")

    processed_path = os.path.join(BASE_DIR, "data/processed")
    os.makedirs(processed_path, exist_ok=True)

    save_json(warehouse, os.path.join(processed_path, "warehouse.json"))

    print("🎯 Transform selesai!")

if __name__ == "__main__":
    run_transform()