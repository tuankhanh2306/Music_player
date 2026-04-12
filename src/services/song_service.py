import os
import uuid
import logging
from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.orm import Session
from src.config import settings
from src.database import crud
from src.audio_processing.feature_extraction import extract_mfcc, update_feature_cache
from src.recommendation.engine import retrain_model
from src.core.exceptions import InvalidAudioFileException

logger = logging.getLogger(__name__)

async def process_upload(db: Session, file: UploadFile, title: str, artist: str, background_tasks: BackgroundTasks):
    """
    Xử lý việc tải lên bài hát:
    1. Lưu file vào uploads/
    2. Ghi database
    3. Thêm background task để trích xuất feature và retrain AI
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

    # 4. Lưu metadata vào DB
    db_song = crud.create_song(db, title=title, artist=artist, filepath=file_path)

    # 5. Thêm Background Task xử lý AI
    background_tasks.add_task(extract_features_and_retrain, db_song.id, file_path)

    return db_song

from src.database.db import SessionLocal

def extract_features_and_retrain(song_id: int, file_path: str):
    """Nhiệm vụ chạy ngầm: Trích xuất MFCC -> Cập nhật Cache -> Huấn luyện lại mô hình."""
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
        
        logger.info(f"Hoàn tất xử lý AI cho song_id={song_id}.")
    except Exception as e:
        logger.error(f"Lỗi xử lý ngầm cho song_id={song_id}: {e}")
    finally:
        db.close()
