"""
Script: backfill_duration.py
Muc dich: Do lai thoi luong thuc te tu file MP3 va cap nhat vao Database
cho tat ca bai hat co duration = 0.
Chay: python backfill_duration.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3

DB_PATH = "music_db.db"

def get_duration(filepath):
    try:
        from mutagen.mp3 import MP3
        from mutagen import File as MutagenFile
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.mp3':
            audio = MP3(filepath)
        else:
            audio = MutagenFile(filepath)
        if audio and audio.info:
            return round(audio.info.length, 2)
    except ModuleNotFoundError:
        try:
            import librosa
            return round(librosa.get_duration(path=filepath), 2)
        except Exception as e:
            print(f"  [WARN] librosa failed for {filepath}: {e}")
    except Exception as e:
        print(f"  [WARN] Cannot read {filepath}: {e}")
    return 0.0


def backfill():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] DB not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filepath, duration FROM songs")
    rows = cursor.fetchall()

    updated = 0
    skipped = 0
    for song_id, filepath, duration in rows:
        if duration and duration > 0:
            skipped += 1
            continue

        if not os.path.exists(filepath):
            print(f"  [SKIP] id={song_id} file not found: {filepath}")
            skipped += 1
            continue

        new_duration = get_duration(filepath)
        if new_duration > 0:
            cursor.execute("UPDATE songs SET duration = ? WHERE id = ?", (new_duration, song_id))
            print(f"  [OK] id={song_id} -> {new_duration}s")
            updated += 1
        else:
            print(f"  [FAIL] id={song_id} could not measure duration")
            skipped += 1

    conn.commit()
    conn.close()
    print(f"\nDone: {updated} updated, {skipped} skipped.")

if __name__ == "__main__":
    backfill()
