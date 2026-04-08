from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema khi User upload bài hát mới
class SongCreate(BaseModel):
    title: str
    artist: str

# Schema khi trả thông tin bài hát về
class SongResponse(BaseModel):
    id: int
    title: str
    artist: str
    duration: Optional[float] = None
    has_features: bool
    created_at: datetime

    class Config:
        from_attributes = True