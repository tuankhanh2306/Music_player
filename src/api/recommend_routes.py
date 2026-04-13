"""
File: src/api/recommend_routes.py
Chức năng: Các endpoint API cho gợi ý bài hát và AI Radio.
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.services import recommend_service
from src.core.exceptions import SongNotFoundException, ModelNotFittedException
from src.database import crud

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

# ⚠️ QUAN TRỌNG: Route /radio/{id} phải đặt TRƯỚC /{song_id}
# Vì FastAPI khớp route theo thứ tự — nếu /{song_id} ở trên,
# FastAPI sẽ thử parse "radio" thành int và trả lỗi 422.

@router.get("/radio/{seed_song_id}", summary="Tạo AI Radio từ một bài hát")
def create_ai_radio(
    seed_song_id: int,
    queue_size: int = Query(default=20, ge=5, le=50, description="Số bài trong queue (5–50)"),
    db: Session = Depends(get_db),
):
    """
    Tạo danh sách phát AI Radio tự động từ một bài hát **seed**.

    **Thuật toán Chaining KNN**:
    1. Bắt đầu từ `seed_song_id`
    2. Tìm bài tương tự nhất (cosine distance trên MFCC vector)
    3. Bài vừa thêm → làm đầu vào tìm tiếp (chaining)
    4. Visited set đảm bảo không lặp bài
    5. Fallback tự động nếu chain bị đứt

    **Trả về**: Danh sách phát theo thứ tự, bắt đầu từ bài seed.
    """
    try:
        queue_ids = recommend_service.build_ai_radio(db, seed_song_id, queue_size=queue_size)
        songs = [crud.get_song(db, sid) for sid in queue_ids]
        songs = [s for s in songs if s]
        return {
            "seed_song_id": seed_song_id,
            "queue_size": len(queue_ids),
            "song_ids": queue_ids,
            "queue": [
                {
                    "id": s.id,
                    "title": s.title,
                    "artist": s.artist,
                    "genre": s.genre,
                    "sub_genres": s.sub_genres,
                    "duration": s.duration,
                    "filepath": s.filepath,
                }
                for s in songs
            ]
        }
    except SongNotFoundException:
        raise HTTPException(status_code=404, detail="Bài hát seed không tồn tại.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ModelNotFittedException:
        raise HTTPException(
            status_code=503,
            detail="Mô hình AI chưa được huấn luyện. Hãy chạy `python backfill_features.py` trước."
        )


@router.get("/{song_id}", summary="Gợi ý bài hát tương tự")
def get_recommendations(
    song_id: int,
    top_k: int = Query(default=5, ge=1, le=20, description="Số bài gợi ý (1–20)"),
    db: Session = Depends(get_db),
):
    """Lấy danh sách top-K bài hát được AI gợi ý tương tự bài đang phát."""
    try:
        recommend_ids = recommend_service.get_recommendations_for_song(db, song_id, top_k)
        songs = [crud.get_song(db, sid) for sid in recommend_ids]
        songs = [s for s in songs if s]
        return {
            "target_song_id": song_id,
            "recommended_ids": recommend_ids,
            "songs": [
                {
                    "id": s.id,
                    "title": s.title,
                    "artist": s.artist,
                    "genre": s.genre,
                    "sub_genres": s.sub_genres,
                    "duration": s.duration,
                    "filepath": s.filepath,
                }
                for s in songs
            ]
        }
    except SongNotFoundException:
        raise HTTPException(status_code=404, detail="Bài hát không tồn tại.")
    except ModelNotFittedException:
        raise HTTPException(
            status_code=503,
            detail="Mô hình AI chưa được huấn luyện. Hãy chạy `python backfill_features.py` trước."
        )
