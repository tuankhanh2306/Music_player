"""
Script: import_songs.py
Chức năng: Quét thư mục `list/`, xóa toàn bộ dữ liệu cũ trong DB,
           copy file nhạc vào `uploads/`, rồi insert bài hát mới với
           đầy đủ thông tin title/artist/genre/subgenre.
Cách chạy: python import_songs.py
"""
import sys
import os
import shutil
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.db import SessionLocal
from src.models.song import Song
from src.models.playlist import Playlist
from src.database.crud import create_song

# ─── Logging ───────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ─── Thư mục ───────────────────────────────────────────────────────────────
LIST_DIR   = os.path.join(os.path.dirname(__file__), "list")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ─── Mapping: (tên artist folder  →  tên ca sĩ chuẩn trong DB) ────────────
ARTIST_MAP = {
    "Sơn Tùng MT-P":     "Sơn Tùng M-TP",
    "Soobin Hoàng Sơn":  "SOOBIN",
    "Vũ":                "Vũ.",
    "Thịnh Suy":         "Thịnh Suy",
    "Đen Vâu":           "Đen Vâu",
    "Alan Walker":       "Alan Walker",
    "Avicii":            "Avicii",
    "Adele":             "Adele",
    "Linkin Park":       "Linkin Park",
    "Microwave":         "Microwave",
    "David Guetta":      "David Guetta",
    "Ed Sheeran":        "Ed Sheeran",
    "Maroon 5":          "Maroon 5",
    "Nirvana":           "Nirvana",
    "Tóc Tiên":          "Tóc Tiên",
}

# ─── Mapping: (artist chuẩn, title chuẩn) → (genre, subgenre) ─────────────
SONG_META = {
    # Sơn Tùng M-TP
    ("Sơn Tùng M-TP", "Nơi Này Có Anh"):       ("Pop",   "Ballad"),
    ("Sơn Tùng M-TP", "Nắng Ấm Xa Dần"):        ("Pop",   "RnB"),
    ("Sơn Tùng M-TP", "Có Chắc Yêu Là Đây"):    ("Pop",   "Contemporary"),
    ("Sơn Tùng M-TP", "Em Của Ngày Hôm Qua"):   ("EDM",   "Dance"),
    ("Sơn Tùng M-TP", "Chạy Ngay Đi"):          ("EDM",   "Trap"),
    ("Sơn Tùng M-TP", "Lạc Trôi"):              ("EDM",   "FutureBass"),
    # Vũ.
    ("Vũ.", "Lạ Lùng"):                         ("Indie", "Acoustic"),
    ("Vũ.", "Bước Qua Nhau"):                   ("Indie", "Acoustic"),
    ("Vũ.", "Đông Kiếm Em"):                    ("Indie", "Acoustic"),
    # SOOBIN
    ("SOOBIN", "Dancing In The Dark"):           ("Pop",   "Synthpop"),
    ("SOOBIN", "Tháng Năm"):                    ("Pop",   "RnB"),
    # Thịnh Suy
    ("Thịnh Suy", "Một Đêm Say"):               ("Indie", "Acoustic"),
    # Đen Vâu
    ("Đen Vâu", "Hai Triệu Năm"):               ("Rap",   "Oldschool"),
    # Alan Walker
    ("Alan Walker", "Faded"):                   ("EDM",   "Electro"),
    # Avicii
    ("Avicii", "Wake Me Up"):                   ("EDM",   "House"),
    # Adele
    ("Adele", "Someone Like You"):              ("Pop",   "Ballad"),
    # Linkin Park
    ("Linkin Park", "Numb"):                    ("Rock",  "Numetal"),
    ("Linkin Park", "In The End"):              ("Rock",  "Numetal"),
    # Microwave
    ("Microwave", "Tìm Lại"):                   ("Rock",  "Numetal"),
    # David Guetta
    ("David Guetta", "Titanium"):               ("EDM",   "House"),
    # Ed Sheeran
    ("Ed Sheeran", "Perfect"):                  ("Pop",   "Ballad"),
    # Maroon 5
    ("Maroon 5", "Memories"):                   ("Pop",   "Contemporary"),
    # Nirvana
    ("Nirvana", "Nirvana"):                     ("Rock",  "Grunge"),
    # Tóc Tiên
    ("Tóc Tiên", "Vũ Điệu Cồng Chiêng"):       ("Pop",   "Contemporary"),
}

# Keywords để match tên file → tên bài hát chuẩn
TITLE_KEYWORDS = {
    "noi nay co anh":       "Nơi Này Có Anh",
    "nang am xa dan":       "Nắng Ấm Xa Dần",
    "co chac yeu la day":   "Có Chắc Yêu Là Đây",
    "em cua ngay hom qua":  "Em Của Ngày Hôm Qua",
    "chay ngay di":         "Chạy Ngay Đi",
    "lac troi":             "Lạc Trôi",
    "la lung":              "Lạ Lùng",
    "buoc qua nhau":        "Bước Qua Nhau",
    "dong kiem em":         "Đông Kiếm Em",
    "dancing in the dark":  "Dancing In The Dark",
    "thang nam":            "Tháng Năm",
    "mot dem say":          "Một Đêm Say",
    "hai trieu nam":        "Hai Triệu Năm",
    "faded":                "Faded",
    "wake me up":           "Wake Me Up",
    "someone like you":     "Someone Like You",
    "numb":                 "Numb",
    "in the end":           "In The End",
    "tim lai":              "Tìm Lại",
    "titanium":             "Titanium",
    "perfect":              "Perfect",
    "memories":             "Memories",
    "nirvana":              "Nirvana",
    "vu dieu cong chieng":  "Vũ Điệu Cồng Chiêng",
}

def normalize(text: str) -> str:
    """Chuyển string về chữ thường, bỏ dấu cơ bản để so khớp."""
    import unicodedata
    text = text.lower()
    # Bỏ dấu tiếng Việt
    nfkd = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Giữ lại chữ cái, số, khoảng trắng
    result = ""
    for c in text:
        if c.isalnum() or c == " ":
            result += c
    return result.strip()

def match_title(filename: str) -> str | None:
    """Cố gắng khớp tên file với title chuẩn qua keywords."""
    norm = normalize(filename)
    for kw, title in TITLE_KEYWORDS.items():
        if kw in norm:
            return title
    return None

def get_duration(filepath: str) -> float:
    """Lấy thời lượng file âm thanh (giây)."""
    try:
        import mutagen
        from mutagen.mp3 import MP3
        audio = MP3(filepath)
        return round(audio.info.length, 2)
    except Exception:
        pass
    try:
        import librosa
        duration = librosa.get_duration(path=filepath)
        return round(duration, 2)
    except Exception:
        pass
    return 0.0

# ─── Xóa toàn bộ dữ liệu cũ ───────────────────────────────────────────────
def clear_old_data(db):
    logger.info("🗑️  Đang xóa toàn bộ dữ liệu cũ...")
    # Xóa playlist_songs (many-to-many) trước
    from src.models.playlist import playlist_song
    db.execute(playlist_song.delete())
    db.query(Playlist).delete()
    db.query(Song).delete()
    db.commit()

    # Xóa toàn bộ file trong uploads/
    for fname in os.listdir(UPLOAD_DIR):
        fpath = os.path.join(UPLOAD_DIR, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)
    logger.info("✅ Đã xóa xong dữ liệu cũ và file uploads.")

# ─── Import chính ──────────────────────────────────────────────────────────
def import_songs():
    db = SessionLocal()
    try:
        clear_old_data(db)

        imported = 0
        skipped  = 0

        for artist_folder in sorted(os.listdir(LIST_DIR)):
            artist_path = os.path.join(LIST_DIR, artist_folder)
            if not os.path.isdir(artist_path):
                continue

            # Chuẩn hóa tên artist
            artist_name = ARTIST_MAP.get(artist_folder, artist_folder)

            for fname in sorted(os.listdir(artist_path)):
                if not any(fname.lower().endswith(ext) for ext in [".mp3", ".wav", ".flac"]):
                    continue

                src_path = os.path.join(artist_path, fname)

                # Xác định title
                title = match_title(os.path.splitext(fname)[0])
                if not title:
                    # Fallback: dùng tên file (bỏ extension)
                    title = os.path.splitext(fname)[0].strip()
                    logger.warning(f"⚠️  Không khớp keyword cho '{fname}' → dùng tên file.")

                # Lấy genre/subgenre
                genre, subgenre = SONG_META.get((artist_name, title), (None, None))

                # Copy file sang uploads/
                dest_fname = f"{artist_name} - {title}{os.path.splitext(fname)[1]}"
                dest_path  = os.path.join(UPLOAD_DIR, dest_fname)
                shutil.copy2(src_path, dest_path)

                # Relative path lưu vào DB
                rel_path = f"uploads/{dest_fname}"

                # Lấy duration
                duration = get_duration(dest_path)

                # Insert vào DB
                song = create_song(
                    db       = db,
                    title    = title,
                    artist   = artist_name,
                    filepath = rel_path,
                    genre    = genre,
                    sub_genres = subgenre,
                    duration = duration,
                )
                logger.info(
                    f"✅ [{song.id:>3}] {artist_name} – {title}  |  "
                    f"{genre}/{subgenre}  |  {duration}s"
                )
                imported += 1

        logger.info(f"\n🎉 HOÀN THÀNH! Import {imported} bài, bỏ qua {skipped} bài.")

    except Exception as e:
        logger.error(f"❌ Lỗi: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_songs()
