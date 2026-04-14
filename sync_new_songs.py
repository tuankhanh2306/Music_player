"""
Script: sync_new_songs.py
Chức năng:
  1. Xóa các bản trùng lặp (ID 25-65) do import 2 lần
  2. Quét thư mục list/ tìm file mới chưa có trong DB
  3. Import bài mới với metadata từ mapping
  4. Chạy MFCC extraction + retrain KNN cho bài mới
Chạy: python sync_new_songs.py
"""
import sys, os, shutil, logging, unicodedata

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

from src.database.db import SessionLocal
from src.models.song import Song
from src.models.playlist import playlist_song
from src.database.crud import create_song, get_all_songs, update_song_feature_status
from src.audio_processing.feature_extraction import extract_mfcc, update_feature_cache
from src.recommendation.engine import retrain_model

LIST_DIR   = os.path.join(os.path.dirname(__file__), "list")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── Mapping: tên folder artist → tên chuẩn trong DB ────────────────────────
ARTIST_MAP = {
    "Sơn Tùng MT-P":      "Sơn Tùng M-TP",
    "Soobin Hoàng Sơn":   "SOOBIN",
    "Vũ":                 "Vũ.",
    "Thịnh Suy":          "Thịnh Suy",
    "Đen Vâu":            "Đen Vâu",
    "Alan Walker":        "Alan Walker",
    "Avicii":             "Avicii",
    "Adele":              "Adele",
    "Linkin Park":        "Linkin Park",
    "Microwave":          "Microwave",
    "David Guetta":       "David Guetta",
    "Ed Sheeran":         "Ed Sheeran",
    "Maroon 5":           "Maroon 5",
    "Nirvana":            "Nirvana",
    "Tóc Tiên":           "Tóc Tiên",
    "BINZ":               "Binz",
    "Wxrdie":             "Wxrdie",
    "MCK":                "MCK",
    "tlinh":              "tlinh",
    "Hoàng Thùy Linh":    "Hoàng Thùy Linh",
    "Phương Ly":          "Phương Ly",
}

# ── Mapping: (artist chuẩn, title chuẩn) → (genre, subgenre) ───────────────
SONG_META = {
    # === BATCH 1 (cũ) ===
    ("Sơn Tùng M-TP", "Nơi Này Có Anh"):        ("Pop",   "Ballad"),
    ("Sơn Tùng M-TP", "Nắng Ấm Xa Dần"):         ("Pop",   "RnB"),
    ("Sơn Tùng M-TP", "Có Chắc Yêu Là Đây"):     ("Pop",   "Contemporary"),
    ("Sơn Tùng M-TP", "Em Của Ngày Hôm Qua"):    ("EDM",   "Dance"),
    ("Sơn Tùng M-TP", "Chạy Ngay Đi"):           ("EDM",   "Trap"),
    ("Sơn Tùng M-TP", "Lạc Trôi"):               ("EDM",   "FutureBass"),
    ("Vũ.", "Lạ Lùng"):                          ("Indie", "Acoustic"),
    ("Vũ.", "Bước Qua Nhau"):                    ("Indie", "Acoustic"),
    ("Vũ.", "Đông Kiếm Em"):                     ("Indie", "Acoustic"),
    ("SOOBIN", "Dancing In The Dark"):            ("Pop",   "Synthpop"),
    ("SOOBIN", "Tháng Năm"):                     ("Pop",   "RnB"),
    ("Thịnh Suy", "Một Đêm Say"):                ("Indie", "Acoustic"),
    ("Đen Vâu", "Hai Triệu Năm"):                ("Rap",   "Oldschool"),
    ("Alan Walker", "Faded"):                    ("EDM",   "Electro"),
    ("Avicii", "Wake Me Up"):                    ("EDM",   "House"),
    ("Adele", "Someone Like You"):               ("Pop",   "Ballad"),
    ("Linkin Park", "Numb"):                     ("Rock",  "Numetal"),
    ("Linkin Park", "In The End"):               ("Rock",  "Numetal"),
    ("Microwave", "Tìm Lại"):                    ("Rock",  "Numetal"),
    ("David Guetta", "Titanium"):                ("EDM",   "House"),
    ("Ed Sheeran", "Perfect"):                   ("Pop",   "Ballad"),
    ("Maroon 5", "Memories"):                    ("Pop",   "Contemporary"),
    ("Nirvana", "Nirvana"):                      ("Rock",  "Grunge"),
    ("Tóc Tiên", "Vũ Điệu Cồng Chiêng"):        ("Pop",   "Contemporary"),
    # === BATCH 2 (mới) ===
    ("Sơn Tùng M-TP", "Âm Thầm Bên Em"):        ("Pop",   "Ballad"),
    ("Sơn Tùng M-TP", "Chắc Ai Đó Sẽ Về"):      ("Pop",   "Ballad"),
    ("Sơn Tùng M-TP", "Khuôn Mặt Đáng Thương"): ("EDM",   "Dance"),
    ("SOOBIN", "Phía Sau Một Cô Gái"):           ("Pop",   "Ballad"),
    ("SOOBIN", "Trò Chơi"):                      ("EDM",   "House"),
    ("SOOBIN", "Daydreams"):                     ("Pop",   "RnB"),
    ("Phương Ly", "Thích Thích"):                ("Pop",   "Ballad"),
    ("Hoàng Thùy Linh", "See Tình"):             ("EDM",   "Dance"),
    ("Hoàng Thùy Linh", "Để Mị Nói Cho Mà Nghe"):("EDM",  "Folktronica"),
    ("Maroon 5", "Sugar"):                       ("Pop",   "Funk"),
    ("Binz", "Gene"):                            ("Rap",   "Trap"),
    ("Binz", "Bigcityboi"):                      ("Rap",   "Trap"),
    ("Binz", "OK"):                              ("Pop",   "RnB"),
    ("MCK", "Tại Vì Sao"):                       ("Rap",   "Trap"),
    ("MCK", "Chìm Sâu"):                         ("Rap",   "Melodic"),
    ("Wxrdie", "LAVIAI"):                        ("Rap",   "Trap"),
    ("Wxrdie", "TETVOVEN"):                      ("Rap",   "Trap"),
    ("tlinh", "Không Cần Phải Nói Nhiều"):       ("Rap",   "Trap"),
    ("tlinh", "Gái Độc Thân"):                   ("Pop",   "RnB"),
    ("Đen Vâu", "Mang Tiền Về Cho Mẹ"):          ("Rap",   "Oldschool"),
    ("Đen Vâu", "Lối Nhỏ"):                      ("Rap",   "Chill"),
}

# ── Keyword → Title chuẩn ───────────────────────────────────────────────────
TITLE_KEYWORDS = {
    # batch 1
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
    # batch 2
    "am tham ben em":       "Âm Thầm Bên Em",
    "chac ai do se ve":     "Chắc Ai Đó Sẽ Về",
    "khuon mat dang thuong":"Khuôn Mặt Đáng Thương",
    "phia sau mot co gai":  "Phía Sau Một Cô Gái",
    "tro choi":             "Trò Chơi",
    "daydreams":            "Daydreams",
    "thich thich":          "Thích Thích",
    "see tinh":             "See Tình",
    "de mi noi cho ma nghe":"Để Mị Nói Cho Mà Nghe",
    "sugar":                "Sugar",
    "gene":                 "Gene",
    "bigcityboi":           "Bigcityboi",
    "ok":                   "OK",
    "tai vi sao":           "Tại Vì Sao",
    "chim sau":             "Chìm Sâu",
    "laviai":               "LAVIAI",
    "tetvoven":             "TETVOVEN",
    "khong can phai noi nhieu": "Không Cần Phải Nói Nhiều",
    "gai doc than":         "Gái Độc Thân",
    "mang tien ve cho me":  "Mang Tiền Về Cho Mẹ",
    "loi nho":              "Lối Nhỏ",
}


def normalize(text: str) -> str:
    text = text.lower()
    nfkd = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in nfkd if not unicodedata.combining(c))
    return "".join(c for c in text if c.isalnum() or c == " ").strip()


def match_title(filename: str):
    norm = normalize(os.path.splitext(filename)[0])
    for kw, title in TITLE_KEYWORDS.items():
        if kw in norm:
            return title
    return None


def get_duration(filepath: str) -> float:
    try:
        from mutagen.mp3 import MP3
        return round(MP3(filepath).info.length, 2)
    except Exception:
        pass
    try:
        import librosa
        return round(librosa.get_duration(path=filepath), 2)
    except Exception:
        return 0.0


# ════════════════════════════════════════════════════════════════════════════
def step1_clean_duplicates(db):
    """Xóa các bài trùng lặp – giữ lại bài có id nhỏ nhất cho mỗi cặp (artist, title)."""
    logger.info("── BƯỚC 1: Dọn dẹp bản sao ──────────────────────────────")
    all_songs = db.query(Song).order_by(Song.id).all()

    seen = {}      # (artist, title) → id đầu tiên (giữ lại)
    to_delete = [] # id cần xóa

    for s in all_songs:
        key = (s.artist.strip().lower(), s.title.strip().lower())
        if key in seen:
            to_delete.append(s.id)
        else:
            seen[key] = s.id

    if not to_delete:
        logger.info("   Không có bản sao nào.")
        return

    logger.info(f"   Tìm thấy {len(to_delete)} bản sao: IDs = {to_delete}")

    # Xóa khỏi playlist_song trước
    from sqlalchemy import text
    for sid in to_delete:
        db.execute(text(f"DELETE FROM playlist_song WHERE song_id = {sid}"))

    db.query(Song).filter(Song.id.in_(to_delete)).delete(synchronize_session=False)
    db.commit()
    logger.info(f"   ✅ Đã xóa {len(to_delete)} bản sao.")


# ════════════════════════════════════════════════════════════════════════════
def step2_import_new(db):
    """Quét list/, tìm file chưa có trong DB và import chúng."""
    logger.info("── BƯỚC 2: Import bài mới ────────────────────────────────")

    # Lấy tập hợp filepath đang có trong DB
    existing_songs = db.query(Song).all()
    # Cũng build set (artist, title) để tránh trùng theo nội dung
    existing_keys = set()
    for s in existing_songs:
        existing_keys.add((s.artist.strip().lower(), s.title.strip().lower()))

    new_song_ids = []
    imported = 0

    for folder in sorted(os.listdir(LIST_DIR)):
        folder_path = os.path.join(LIST_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        artist_name = ARTIST_MAP.get(folder, folder)

        for fname in sorted(os.listdir(folder_path)):
            if not any(fname.lower().endswith(ext) for ext in [".mp3", ".wav", ".flac"]):
                continue

            src_path = os.path.join(folder_path, fname)

            # Xác định title
            title = match_title(fname)
            if not title:
                title = os.path.splitext(fname)[0].strip()

            # Kiểm tra đã có trong DB chưa
            key = (artist_name.strip().lower(), title.strip().lower())
            if key in existing_keys:
                continue  # Đã có → bỏ qua

            # Lấy genre/subgenre
            genre, subgenre = SONG_META.get((artist_name, title), (None, None))

            # Copy file sang uploads/
            ext = os.path.splitext(fname)[1]
            dest_fname = f"{artist_name} - {title}{ext}"
            dest_path  = os.path.join(UPLOAD_DIR, dest_fname)
            if not os.path.exists(dest_path):
                shutil.copy2(src_path, dest_path)

            rel_path = f"uploads/{dest_fname}"
            duration = get_duration(dest_path)

            song = create_song(
                db=db,
                title=title,
                artist=artist_name,
                filepath=rel_path,
                genre=genre,
                sub_genres=subgenre,
                duration=duration,
            )
            existing_keys.add(key)
            new_song_ids.append(song.id)
            logger.info(f"   ✅ [{song.id:>3}] {artist_name} – {title}  |  {genre}/{subgenre}  |  {duration:.0f}s")
            imported += 1

    logger.info(f"   Tổng cộng import {imported} bài mới.")
    return new_song_ids


# ════════════════════════════════════════════════════════════════════════════
def step3_extract_mfcc(db, new_song_ids: list):
    """Trích xuất MFCC cho các bài mới import."""
    logger.info("── BƯỚC 3: Trích xuất MFCC ───────────────────────────────")

    # Lấy tất cả bài chưa có features (bao gồm cả bài cũ nếu còn sót)
    pending = db.query(Song).filter(Song.has_features == False).all()

    if not pending:
        logger.info("   Tất cả bài đã có features.")
        return

    logger.info(f"   {len(pending)} bài cần trích xuất MFCC...")
    success = fail = 0

    for i, song in enumerate(pending, 1):
        filepath = song.filepath
        if not os.path.exists(filepath):
            filepath = os.path.join(os.path.dirname(__file__), filepath)
        if not os.path.exists(filepath):
            logger.warning(f"   [{i}/{len(pending)}] ❌ File không tồn tại: {song.filepath}")
            fail += 1
            continue

        logger.info(f"   [{i}/{len(pending)}] 🎵 {song.artist} – {song.title}")
        try:
            vec = extract_mfcc(filepath)
            update_feature_cache(song.id, vec)
            update_song_feature_status(db, song.id, has_features=True)
            logger.info(f"              ✅ Vector shape: {vec.shape}")
            success += 1
        except Exception as e:
            logger.error(f"              ❌ Lỗi: {e}")
            fail += 1

    logger.info(f"\n   Kết quả MFCC: ✅ {success} thành công, ❌ {fail} thất bại")


# ════════════════════════════════════════════════════════════════════════════
def main():
    db = SessionLocal()
    try:
        # Bước 1: Dọn bản sao
        step1_clean_duplicates(db)

        # Bước 2: Import bài mới
        new_ids = step2_import_new(db)

        # Bước 3: MFCC cho bài mới
        step3_extract_mfcc(db, new_ids)

        # Bước 4: Retrain toàn bộ model
        logger.info("── BƯỚC 4: Retrain KNN Model ─────────────────────────────")
        retrain_model()

        # Tổng kết
        total = db.query(Song).count()
        has_feat = db.query(Song).filter(Song.has_features == True).count()
        logger.info(f"""
╔══════════════════════════════════════════╗
║           SYNC HOÀN TẤT ✅              ║
╠══════════════════════════════════════════╣
║  Bài mới import  : {len(new_ids):<4}                    ║
║  Tổng trong DB   : {total:<4}                    ║
║  Đã có MFCC      : {has_feat:<4}/{total:<4}               ║
╚══════════════════════════════════════════╝""")

    except Exception as e:
        logger.error(f"❌ Lỗi: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
