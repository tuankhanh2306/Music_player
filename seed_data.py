import sys
import os

# Thêm dòng này để Python nhận diện được thư mục src khi chạy script trực tiếp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db import SessionLocal
from src.database.crud import create_user, create_song, create_playlist, add_song_to_playlist

def seed():
    db = SessionLocal()
    try:
        print("⏳ Bắt đầu nạp dữ liệu (seed data)...")
        
        # 1. Tạo User (Tạm thời dùng password giả vì chưa code hệ thống Auth)
        user = create_user(db, "admin", "admin@music.com", "hashed_password_mock")
        print(f"✅ Đã tạo user: {user.username}")

        # 2. Tạo 5 Bài hát mẫu
        songs_data = [
            ("Lạc Trôi", "Sơn Tùng M-TP", "uploads/mock1.mp3"),
            ("Shape of You", "Ed Sheeran", "uploads/mock2.mp3"),
            ("Blinding Lights", "The Weeknd", "uploads/mock3.mp3"),
            ("Nơi Này Có Anh", "Sơn Tùng M-TP", "uploads/mock4.mp3"),
            ("Waiting For You", "MONO", "uploads/mock5.mp3")
        ]
        
        song_ids = []
        for title, artist, filepath in songs_data:
            song = create_song(db, title, artist, filepath, user.id)
            song_ids.append(song.id)
        print("✅ Đã tạo 5 bài hát mẫu.")

        # 3. Tạo Playlist và thêm bài hát số 1 và số 3 vào playlist
        playlist = create_playlist(db, "EDM & Chill", user.id)
        add_song_to_playlist(db, playlist.id, song_ids[0])
        add_song_to_playlist(db, playlist.id, song_ids[2])
        print(f"✅ Đã tạo playlist '{playlist.name}' và thêm nhạc thành công.")

        print("🎉 QUÁ TRÌNH SEED DATA HOÀN TẤT!")

    except Exception as e:
        print(f"❌ Lỗi khi seed data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()