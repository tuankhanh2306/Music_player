from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.schemas.song_schema import SongResponse, SongUpdate
from src.services import song_service
from src.core.exceptions import SongNotFoundException

router = APIRouter(prefix="/songs", tags=["Songs"])

@router.post("/upload", response_model=SongResponse)
async def upload_song(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    artist: str = Form(...),
    genre: str = Form(None),
    sub_genres: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Tải lên bài hát mới và xử lý AI ngầm."""
    return await song_service.process_upload(
        db, file, title, artist, background_tasks,
        genre=genre or None, sub_genres=sub_genres or None
    )

@router.get("/", response_model=List[SongResponse])
def list_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách bài hát (có phân trang)."""
    from src.database import crud
    return crud.get_all_songs(db, skip=skip, limit=limit)

@router.get("/{song_id}", response_model=SongResponse)
def get_song_detail(song_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết một bài hát."""
    from src.database import crud
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    return song

@router.patch("/{song_id}", response_model=SongResponse)
def update_song(song_id: int, update_data: SongUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin tiêu đề/nghệ sĩ/thể loại của bài hát."""
    from src.database import crud
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    updated = crud.update_song_metadata(
        db, song_id,
        title=update_data.title,
        artist=update_data.artist,
        genre=update_data.genre,
        sub_genres=update_data.sub_genres
    )
    return updated

@router.delete("/{song_id}")
def delete_song(song_id: int, db: Session = Depends(get_db)):
    """Xóa vĩnh viễn hệ thống một bài hát."""
    return song_service.delete_song(db, song_id)

@router.get("/{song_id}/stream")
def stream_song(song_id: int, db: Session = Depends(get_db)):
    """Stream file audio của bài hát."""
    from src.database import crud
    song = crud.get_song(db, song_id)
    if not song or not os.path.exists(song.filepath):
        raise SongNotFoundException("File nhạc không tồn tại trên server.")
    
    return FileResponse(song.filepath, media_type="audio/mpeg")

import os # Cần import os cho stream_song
