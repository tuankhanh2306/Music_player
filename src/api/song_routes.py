from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.schemas.song_schema import SongResponse, SongUpdate, LyricUpdate
from src.services import song_service
from src.core.exceptions import SongNotFoundException
from pydantic import BaseModel

class ConfirmUploadRequest(BaseModel):
    title: str
    artist: str
    genre: str
    temp_path: str

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

@router.post("/analyze")
async def analyze_song_route(file: UploadFile = File(...)):
    """Bước 1: Tải file lên và AI phân tích thể loại."""
    return await song_service.analyze_song(file)

@router.post("/confirm", response_model=SongResponse)
def confirm_upload_route(
    background_tasks: BackgroundTasks,
    request: ConfirmUploadRequest,
    db: Session = Depends(get_db)
):
    """Bước 2: Xác nhận và lưu kết quả AI."""
    return song_service.confirm_upload(
        db=db,
        title=request.title,
        artist=request.artist,
        genre=request.genre,
        temp_path=request.temp_path,
        background_tasks=background_tasks
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

@router.get("/{song_id}/lyrics")
def get_song_lyrics(song_id: int, db: Session = Depends(get_db)):
    """
    Lấy lời bài hát dạng LRC cho bài hát theo ID.
    Trả về has_lyrics=False nếu Whisper chưa xử lý xong.
    """
    from src.database import crud
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    return {
        "song_id": song_id,
        "has_lyrics": bool(song.lrc_content),
        "lrc_content": song.lrc_content or None
    }

@router.put("/{song_id}/lyrics")
def update_song_lyrics(song_id: int, body: LyricUpdate, db: Session = Depends(get_db)):
    """
    Cập nhật nội dung LRC cho bài hát.
    Người dùng chỉnh sửa thủ công từ giao diện và gọi endpoint này để lưu lại.
    """
    from src.database import crud
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    updated = crud.update_song_lrc(db, song_id, body.lrc_content)
    return {
        "song_id": song_id,
        "has_lyrics": True,
        "lrc_content": updated.lrc_content
    }

import os  # Cần import os cho stream_song
