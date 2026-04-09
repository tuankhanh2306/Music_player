import sys
import os

# Thêm root vào path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db import SessionLocal
from src.database.crud import get_all_songs, get_playlist_songs
from src.models.playlist import Playlist

def test_db_content():
    db = SessionLocal()
    try:
        print("\n--- 🎵 KIỂM TRA DỮ LIỆU TRONG DATABASE ---")
        
        # 1. Kiểm tra danh sách bài hát
        songs = get_all_songs(db)
        print(f"\n[1] Tổng số bài hát: {len(songs)}")
        for s in songs:
            print(f"    - ID: {s.id} | {s.title} - {s.artist}")

        # 2. Kiểm tra Playlist
        playlist = db.query(Playlist).first()
        if playlist:
            print(f"\n[2] Playlist tìm thấy: '{playlist.name}' (ID: {playlist.id})")
            p_songs = get_playlist_songs(db, playlist.id)
            print(f"    Dưới đây là các bài hát trong playlist này:")
            for ps in p_songs:
                print(f"    - {ps.title}")
        else:
            print("\n[2] Chưa có playlist nào.")

        print("\n--- ✅ TEST HOÀN TẤT ---")

    except Exception as e:
        print(f"❌ Có lỗi khi truy vấn: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_db_content()
