import sqlite3
import os

db_path = 'music_db.db'
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found")
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check current columns
cur.execute("PRAGMA table_info(songs)")
cols = [row[1] for row in cur.fetchall()]
print('Current columns:', cols)

if 'lrc_content' not in cols:
    print('Adding column lrc_content...')
    cur.execute('ALTER TABLE songs ADD COLUMN lrc_content TEXT DEFAULT NULL')
    conn.commit()
    print('Column added successfully!')
else:
    print('Column lrc_content already exists.')

conn.close()
