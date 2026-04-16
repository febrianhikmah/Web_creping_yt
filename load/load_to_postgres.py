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

        # (SEMUA QUERY LO TETEP SAMA)

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
