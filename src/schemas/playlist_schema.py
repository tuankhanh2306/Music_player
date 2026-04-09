from pydantic import BaseModel
from datetime import datetime
from typing import List
from src.schemas.song_schema import SongResponse

# Schema khi tạo Playlist mới
class PlaylistCreate(BaseModel):
    name: str

# Schema khi trả thông tin Playlist (kèm theo danh sách bài hát bên trong)
class PlaylistResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    songs: List[SongResponse] = []

    class Config:
        from_attributes = True