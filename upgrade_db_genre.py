"""
Script: upgrade_db_genre.py
Mục đích: Thêm cột 'genre' vào bảng 'songs' trong database hiện tại.
Chạy 1 lần duy nhất: python upgrade_db_genre.py
"""
import sqlite3
import os

DB_PATH = "music_db.db"

def upgrade():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] DB file not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(songs)")
    columns = [row[1] for row in cursor.fetchall()]

    if "genre" in columns:
        print("[OK] Column 'genre' already exists. No upgrade needed.")
    else:
        cursor.execute("ALTER TABLE songs ADD COLUMN genre TEXT")
        conn.commit()
        print("[OK] Column 'genre' added to 'songs' table successfully!")

    conn.close()

if __name__ == "__main__":
    upgrade()
