import sqlite3
import os

db_path = "music_db.db"
if not os.path.exists(db_path):
    print(f"Database {db_path} not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT filepath FROM songs LIMIT 10;")
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])
    except Exception as e:
        print(f"Error: {e}")
    conn.close()
