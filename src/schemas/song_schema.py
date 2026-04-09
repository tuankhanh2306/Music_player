"""
File: src/schemas/song_schema.py
Chức năng: Định nghĩa các kiểu dữ liệu (Pydantic models) cho API Bài hát.
Nhiệm vụ: Kiểm tra tính hợp lệ của dữ liệu đầu vào (Create) và định dạng dữ liệu đầu ra (Response).
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SongBase(BaseModel):
    title: str
    artist: str

class SongCreate(SongBase):
    filepath: str

class SongUpdate(BaseModel):
    title: str | None = None
    artist: str | None = None

class SongResponse(SongBase):
    id: int
    filepath: str
    duration: float
    has_features: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
