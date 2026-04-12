from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.services import recommend_service

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.get("/{song_id}")
def get_recommendations(song_id: int, top_k: int = 5, db: Session = Depends(get_db)):
    """Lấy danh sách ID các bài hát được gợi ý của thuật toán AI."""
    recommend_ids = recommend_service.get_recommendations_for_song(db, song_id, top_k)
    return {"target_song_id": song_id, "recommended_ids": recommend_ids}
