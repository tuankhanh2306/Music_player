"""
File: src/seed_data.py
Chức năng: Script nạp dữ liệu mẫu (Seed data).
Nhiệm vụ: Tạo sẵn một số bài hát và playlist mẫu trong DB để phục vụ việc phát triển và test UI.
"""
import sys
import os
import logging

# Thêm root vào path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db import SessionLocal
from src.database.crud import create_song, create_playlist, add_song_to_playlist

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def seed():
    db = SessionLocal()
    try:
        logger.info("⏳ Starting Seed Data (v2.1 No-Auth)...")
        
        # 1. Create 5 sample songs
        songs_data = [
            ("Lac Troi", "Son Tung M-TP", "uploads/mock1.mp3"),
            ("Shape of You", "Ed Sheeran", "uploads/mock2.mp3"),
            ("Blinding Lights", "The Weeknd", "uploads/mock3.mp3"),
            ("Noi Nay Co Anh", "Son Tung M-TP", "uploads/mock4.mp3"),
            ("Waiting For You", "MONO", "uploads/mock5.mp3")
        ]
        
        song_ids = []
        for title, artist, filepath in songs_data:
            song = create_song(db, title, artist, filepath)
            song_ids.append(song.id)
        logger.info(f"✅ Created {len(song_ids)} songs.")

        # 2. Create Playlist
        playlist = create_playlist(db, "EDM & Chill")
        
        # 3. Add 3 songs to playlist
        add_song_to_playlist(db, playlist.id, song_ids[0])
        add_song_to_playlist(db, playlist.id, song_ids[1])
        add_song_to_playlist(db, playlist.id, song_ids[2])
        logger.info(f"✅ Created playlist '{playlist.name}' with 3 songs.")

        logger.info("🎉 SEED DATA COMPLETE!")

    except Exception as e:
        logger.error(f"❌ Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
