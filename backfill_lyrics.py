"""
File: backfill_lyrics.py
Chức năng: Chạy AI Whisper cho toàn bộ bài hát đang có trong DB mà chưa có lời (lrc_content IS NULL).
"""
import os
import sys

# Thêm đường dẫn gốc vào python path để tránh lỗi import src
sys.path.append(os.path.abspath(os.curdir))

import logging
from src.database.db import SessionLocal
from src.database import crud
from src.audio_processing.whisper_service import transcribe_to_lrc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    db = SessionLocal()
    try:
        # Lấy tất cả bài hát chưa có lyrics
        songs = crud.get_all_songs(db)
        songs_to_process = [s for s in songs if not s.lrc_content]
        
        if not songs_to_process:
            logger.info("Tất cả bài hát đều đã có lời hoặc không có bài hát nào trong DB.")
            return

        logger.info(f"Phát hiện {len(songs_to_process)} bài hát cần tạo lời nhạc...")

        for song in songs_to_process:
            logger.info(f"Đang xử lý: {song.title} - {song.artist}")
            
            if not os.path.exists(song.filepath):
                logger.warning(f"File không tồn tại tại: {song.filepath}. Bỏ qua.")
                continue

            try:
                lrc = transcribe_to_lrc(song.filepath)
                if lrc:
                    crud.update_song_lrc(db, song.id, lrc)
                    logger.info(f"Đã tạo lời thành công cho: {song.title}")
                else:
                    logger.warning(f"Whisper không thể tạo lời cho: {song.title}")
            except Exception as e:
                logger.error(f"Lỗi khi xử lý {song.title}: {e}")

        logger.info("Hoàn tất quá trình tạo lời nhạc cho thư viện cũ.")

    finally:
        db.close()

if __name__ == "__main__":
    main()
