"""
File: src/schemas/playlist_schema.py
Chức năng: Định nghĩa các kiểu dữ liệu cho API Playlist.
Nhiệm vụ: Quy định định dạng JSON trả về khi truy vấn danh sách playlist.
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from src.schemas.song_schema import SongResponse

class PlaylistBase(BaseModel):
    name: str

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistResponse(PlaylistBase):
    id: int
    created_at: datetime
    songs: List[SongResponse] = []

    model_config = ConfigDict(from_attributes=True)
