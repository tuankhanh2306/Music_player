"""
Script: fix_titles.py - Làm sạch tên bài hát thừa chữ trong DB
"""
import sqlite3

conn = sqlite3.connect('music_db.db')
cur = conn.cursor()

# Format: (id, title_mới_đúng)
FIXES = [
    (33,  "Để Mị Nói Cho Mà Nghe"),
    (35,  "Chìm Sâu"),
    (36,  "Tại Vì Sao"),
    (40,  "Thích Thích"),
    (62,  "Gái Độc Thân"),
]

for song_id, new_title in FIXES:
    cur.execute("UPDATE songs SET title = ? WHERE id = ?", (new_title, song_id))
    print(f"[{song_id}] → {new_title}")

conn.commit()
conn.close()
print("\n✅ Done!")
