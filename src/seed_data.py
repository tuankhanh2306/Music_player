import sys
import os
import logging

# Thêm dòng này để Python nhận diện được thư mục src khi chạy script trực tiếp
# Cấu trúc: Music-player/src/seed_data.py -> thêm Music-player/ vào path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db import SessionLocal
from src.database.crud import create_song, create_playlist, add_song_to_playlist

# Cấu hình logging để thay cho print()
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def seed():
    db = SessionLocal()
    try:
        logger.info("⏳ Bắt đầu nạp dữ liệu (seed data) cho v2.1...")
        
        # 1. Tạo 5 Bài hát mẫu (Không có uploaded_by)
        songs_data = [
            ("Lạc Trôi", "Sơn Tùng M-TP", "uploads/mock1.mp3"),
            ("Shape of You", "Ed Sheeran", "uploads/mock2.mp3"),
            ("Blinding Lights", "The Weeknd", "uploads/mock3.mp3"),
            ("Nơi Này Có Anh", "Sơn Tùng M-TP", "uploads/mock4.mp3"),
            ("Waiting For You", "MONO", "uploads/mock5.mp3")
        ]
        
        song_ids = []
        for title, artist, filepath in songs_data:
            song = create_song(db, title, artist, filepath)
            song_ids.append(song.id)
        logger.info(f"✅ Đã tạo {len(song_ids)} bài hát mẫu.")

        # 2. Tạo Playlist (Không có owner_id)
        playlist = create_playlist(db, "EDM & Chill")
        
        # 3. Thêm 3 bài hát vào playlist (Số 1, 2 và 3) theo yêu cầu Track 1.6
        add_song_to_playlist(db, playlist.id, song_ids[0])
        add_song_to_playlist(db, playlist.id, song_ids[1])
        add_song_to_playlist(db, playlist.id, song_ids[2])
        logger.info(f"✅ Đã tạo playlist '{playlist.name}' và thêm 3 bài nhạc thành công.")

        logger.info("🎉 QUÁ TRÌNH SEED DATA HOÀN TẤT!")

    except Exception as e:
        logger.error(f"❌ Lỗi khi seed data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()