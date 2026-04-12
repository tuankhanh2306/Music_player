from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.schemas.playlist_schema import PlaylistResponse, PlaylistCreate, SmartPlaylistCreate
from src.schemas.song_schema import SongResponse
from src.services import playlist_service

router = APIRouter(prefix="/playlists", tags=["Playlists"])

@router.post("/", response_model=PlaylistResponse)
def create_playlist(playlist_in: PlaylistCreate, db: Session = Depends(get_db)):
    """Tạo mới một playlist."""
    return playlist_service.create_new_playlist(db, playlist_in.name)

@router.post("/smart", response_model=PlaylistResponse)
def create_smart_playlist(playlist_in: SmartPlaylistCreate, db: Session = Depends(get_db)):
    """Tạo Smart Playlist tự động bằng cách dùng AI gợi ý nhạc tương đồng."""
    return playlist_service.create_smart_playlist(
        db, 
        song_id=playlist_in.song_id, 
        limit=playlist_in.limit, 
        name=playlist_in.name
    )

@router.post("/{playlist_id}/songs/{song_id}")
def add_song_to_playlist(playlist_id: int, song_id: int, db: Session = Depends(get_db)):
    """Thêm một bài hát vào playlist."""
    return playlist_service.add_song(db, playlist_id, song_id)

@router.get("/{playlist_id}/songs", response_model=List[SongResponse])
def get_playlist_songs(playlist_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách các bài hát trong playlist."""
    return playlist_service.get_songs(db, playlist_id)

@router.get("/", response_model=List[PlaylistResponse])
def list_playlists(db: Session = Depends(get_db)):
    """Lấy danh sách toàn bộ playlist."""
    return playlist_service.get_all_playlists(db)

@router.delete("/{playlist_id}/songs/{song_id}")
def remove_song_from_playlist(playlist_id: int, song_id: int, db: Session = Depends(get_db)):
    """Xóa một bài hát khỏi playlist."""
    return playlist_service.remove_song(db, playlist_id, song_id)

@router.delete("/{playlist_id}")
def delete_playlist(playlist_id: int, db: Session = Depends(get_db)):
    """Xóa toàn bộ playlist."""
    return playlist_service.delete_playlist(db, playlist_id)
