import os
import uuid
import logging
from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.orm import Session
from src.config import settings
from src.database import crud
from src.audio_processing.feature_extraction import extract_mfcc, update_feature_cache, remove_song_from_cache, FeatureExtractionException
from src.recommendation.engine import retrain_model, predict_genre_with_confidence
from src.core.exceptions import InvalidAudioFileException

logger = logging.getLogger(__name__)

def _get_audio_duration(file_path: str) -> float:
    """Trích xuất thời lượng (giây) từ file audio bằng mutagen, fallback sang librosa nếu thiếu mutagen."""
    try:
        from mutagen.mp3 import MP3
        from mutagen.mp4 import MP4
        from mutagen.oggvorbis import OggVorbis
        from mutagen import File as MutagenFile
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.mp3':
            audio = MP3(file_path)
        elif ext in ('.m4a', '.mp4', '.aac'):
            audio = MP4(file_path)
        elif ext == '.ogg':
            audio = OggVorbis(file_path)
        else:
            audio = MutagenFile(file_path)
        
        if audio and audio.info:
            return round(audio.info.length, 2)
    except ModuleNotFoundError:
        logger.warning(f"Không tìm thấy mutagen, dùng librosa đo thời lượng file {file_path}")
        try:
            import librosa
            return round(librosa.get_duration(path=file_path), 2)
        except Exception as e:
            logger.warning(f"Không đo được thời lượng file bằng librosa {file_path}: {e}")
    except Exception as e:
        logger.warning(f"Không đo được thời lượng file {file_path}: {e}")
    return 0.0

async def process_upload(db: Session, file: UploadFile, title: str, artist: str, background_tasks: BackgroundTasks, genre: str | None = None, sub_genres: str | None = None):
    """
    Xử lý việc tải lên bài hát:
    1. Lưu file vào uploads/
    2. Đo thời lượng từ file MP3 bằng mutagen
    3. Ghi database (kèm genre chính, sub_genres, và duration)
    4. Thêm background task để trích xuất feature và retrain AI
    """
    # 1. Validate extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise InvalidAudioFileException(f"Định dạng {file_ext} không hỗ trợ.")

    # 2. Tạo tên file an toàn
    safe_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    # 3. Lưu file vật lý
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        logger.error(f"Lỗi khi lưu file: {e}")
        raise InvalidAudioFileException("Không thể lưu file vào server.")

    # 4. Đo thời lượng thực tế từ file
    duration = _get_audio_duration(file_path)
    logger.info(f"Thời lượng file '{file.filename}': {duration}s")

    # 5. Lưu metadata vào DB
    db_song = crud.create_song(
        db, title=title, artist=artist, filepath=file_path,
        genre=genre or None, sub_genres=sub_genres or None, duration=duration
    )

    # 6. Thêm Background Task xử lý AI
    background_tasks.add_task(extract_features_and_retrain, db_song.id, file_path, genre)

    return db_song

async def analyze_song(file: UploadFile) -> dict:
    """Bước 1: Trích xuất đặc trưng và dự đoán thể loại + Confidence Score (không lưu DB)."""
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise InvalidAudioFileException(f"Định dạng {file_ext} không hỗ trợ.")

    temp_filename = f"temp_{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, temp_filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        logger.error(f"Lỗi khi lưu file temp: {e}")
        raise InvalidAudioFileException("Không thể lưu file tạm.")

    try:
        vector = extract_mfcc(file_path)
        genre, confidence = predict_genre_with_confidence(vector)
        return {
            "temp_path": file_path,
            "predicted_genre": genre or "Unknown",
            "confidence": confidence
        }
    except Exception as e:
        logger.error("Lỗi khi analyze song: %s", e)
        return {
            "temp_path": file_path,
            "predicted_genre": "Unknown",
            "confidence": 0.0
        }

def confirm_upload(db: Session, title: str, artist: str, genre: str, temp_path: str, background_tasks: BackgroundTasks):
    """Bước 2: Người dùng xác nhận, đổi tên file và lưu vào DB."""
    if not os.path.exists(temp_path):
        raise InvalidAudioFileException("File tạm không tồn tại hoặc đã bị xóa.")

    file_ext = os.path.splitext(temp_path)[1].lower()
    final_filename = f"{uuid.uuid4()}{file_ext}"
    final_path = os.path.join(settings.UPLOAD_DIR, final_filename)
    
    os.rename(temp_path, final_path)
    
    duration = _get_audio_duration(final_path)
    
    db_song = crud.create_song(
        db, title=title, artist=artist, filepath=final_path,
        genre=genre, sub_genres=None, duration=duration
    )
    
    background_tasks.add_task(extract_features_and_retrain, db_song.id, final_path, genre)
    return db_song

from src.database.db import SessionLocal

def extract_features_and_retrain(song_id: int, file_path: str, genre: str | None = None):
    """Nhiệm vụ chạy ngầm: Trích xuất MFCC -> Cập nhật Cache -> Huấn luyện lại mô hình -> Dự đoán genre nếu chưa có."""
    db = SessionLocal()
    try:
        logger.info(f"Bắt đầu trích xuất features cho song_id={song_id}...")
        mfcc_vector = extract_mfcc(file_path)
        
        # Cập nhật cache file (.npy)
        update_feature_cache(song_id, mfcc_vector)
        
        # Cập nhật DB status
        crud.update_song_feature_status(db, song_id, has_features=True)
        
        # Retrain mô hình KNN
        retrain_model()
        
        # Nếu người dùng để trống Genre, nhờ AI tự đoán
        if not genre:
            try:
                from src.recommendation.engine import predict_genre
                predicted = predict_genre(song_id)
                if predicted:
                    crud.update_song_metadata(db, song_id, genre=predicted)
                    logger.info(f"AI đoán genre song_id={song_id}: '{predicted}'")
            except Exception as e:
                logger.warning(f"Không thể dự đoán genre cho song_id={song_id}: {e}")
        
        logger.info(f"Hoàn tất xử lý AI cho song_id={song_id}.")
    except Exception as e:
        logger.error(f"Lỗi xử lý ngầm cho song_id={song_id}: {e}")
    finally:
        db.close()

from src.schemas.song_schema import SongUpdate

def update_song(db: Session, song_id: int, update_data: SongUpdate):
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    
    updated_song = crud.update_song_metadata(
        db, 
        song_id, 
        title=update_data.title, 
        artist=update_data.artist
    )
    return updated_song

def delete_song(db: Session, song_id: int):
    """
    Xóa toàn bộ dữ liệu của bài hát: File ổ cứng, Record Database, MFCC Cache, và Retrain.
    """
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    
    filepath = song.filepath
    
    # 1. Xóa file khỏi ổ cứng
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            logger.info(f"Đã xóa file audio: {filepath}")
        except Exception as e:
            logger.error(f"Không thể xóa file {filepath}: {e}")
            
    # 2. Xóa khỏi DB (Tự động trigger CASCADE tới Playlist_Song)
    success = crud.delete_song(db, song_id)
    
    if success:
        # 3. Yêu cầu AI Engine loại bỏ vector ra khỏi cache
        remove_song_from_cache(song_id)
        
        # 4. Huấn luyện lại model
        try:
            retrain_model()
        except Exception as e:
            logger.warning(f"Lỗi khi retrain sau khi xoá: {e}")
            
        return {"message": "Đã xóa bài hát vĩnh viễn khỏi toàn hệ thống."}
    else:
        raise Exception("Lỗi khi xóa bài hát khỏi cơ sở dữ liệu.")
