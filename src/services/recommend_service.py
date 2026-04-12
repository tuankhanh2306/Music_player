import logging
from sqlalchemy.orm import Session
from typing import List

from src.database import crud
from src.recommendation import engine
from src.core.exceptions import SongNotFoundException, ModelNotFittedException

logger = logging.getLogger(__name__)

def get_recommendations_for_song(db: Session, song_id: int, top_k: int = 5) -> List[int]:
    """
    Kết nối Engine AI để trả về các bài hát tương tự.
    """
    # 1. Kiểm tra bài hát có tồn tại không
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    
    # 2. Kiểm tra trạng thái features
    if not song.has_features:
        logger.warning(f"Bài hát {song_id} chưa được trích xuất đặc trưng.")
        return []

    # 3. Gọi engine lấy danh sách ID
    try:
        recommend_ids = engine.get_similar_songs(song_id, top_k=top_k)
        return recommend_ids
    except ModelNotFittedException:
        logger.error("Mô hình KNN chưa được huấn luyện.")
        raise
    except Exception as e:
        logger.error(f"Lỗi khi lấy gợi ý cho bài hát {song_id}: {e}")
        return []
