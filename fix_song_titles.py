"""
Script: fix_song_titles.py
Fix tên và genre cho các bài bị lỗi encoding khi import.
Chạy: python fix_song_titles.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
from src.database.db import SessionLocal
from src.models.song import Song

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Danh sách fix: (artist, title_cũ_chứa_keyword, title_mới, genre, subgenre)
FIXES = [
    ("Sơn Tùng M-TP", "CH",  "Chạy Ngay Đi",      "EDM",   "Trap"),
    ("Sơn Tùng M-TP", "C",   "Có Chắc Yêu Là Đây","Pop",   "Contemporary"),
    ("Thịnh Suy",     "Th",  "Một Đêm Say",        "Indie", "Acoustic"),
    ("Tóc Tiên",      "V",   "Vũ Điệu Cồng Chiêng","Pop",   "Contemporary"),
    ("Vũ.",           "NG",  "Đông Kiếm Em",       "Indie", "Acoustic"),
]

def fix_titles():
    db = SessionLocal()
    try:
        songs = db.query(Song).all()
        fixed = 0

        for song in songs:
            for artist, kw, new_title, genre, subgenre in FIXES:
                if song.artist == artist and (song.genre is None or song.genre == "None"):
                    # Match dựa trên ký tự đầu của title hiện tại
                    if song.title.startswith(kw):
                        old_title = song.title
                        song.title     = new_title
                        song.genre     = genre
                        song.sub_genres = subgenre
                        db.commit()
                        db.refresh(song)
                        logger.info(f"✅ Fixed [{song.id}] '{old_title}' → '{new_title}' ({genre}/{subgenre})")
                        fixed += 1
                        break

        logger.info(f"\n🎉 Fixed {fixed} bài hát.")
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_titles()
