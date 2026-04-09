"""
File: src/check_db.py
Chức năng: Script kiểm tra nhanh dữ liệu trong Database.
Nhiệm vụ: Truy vấn và in ra terminal danh sách bài hát/playlist hiện có (hỗ trợ ASCII cho terminal Windows).
"""
import sys
import os

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db import SessionLocal
from src.database.crud import get_all_songs, get_playlist_songs
from src.models.playlist import Playlist

def test_db_content():
    db = SessionLocal()
    try:
        print("\n--- DATABASE CONTENT CHECK ---")
        
        # 1. Check Songs
        songs = get_all_songs(db)
        print(f"\n[1] Total songs in DB: {len(songs)}")
        for s in songs:
            # Safe encoding for ASCII terminals
            title = s.title.encode('ascii', 'ignore').decode('ascii')
            artist = s.artist.encode('ascii', 'ignore').decode('ascii')
            print(f"    - ID: {s.id} | {title} - {artist}")

        # 2. Check Playlists
        playlist = db.query(Playlist).first()
        if playlist:
            p_name = playlist.name.encode('ascii', 'ignore').decode('ascii')
            print(f"\n[2] Playlist found: '{p_name}' (ID: {playlist.id})")
            p_songs = get_playlist_songs(db, playlist.id)
            print(f"    Songs in this playlist:")
            for ps in p_songs:
                ps_title = ps.title.encode('ascii', 'ignore').decode('ascii')
                print(f"    - {ps_title}")
        else:
            print("\n[2] No playlists found.")

        print("\n--- TEST COMPLETE ---")

    except Exception as e:
        print(f"Error during query: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_db_content()
