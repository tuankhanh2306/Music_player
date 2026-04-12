"""
File: src/models/song.py
Chức năng: Định nghĩa cấu trúc bảng Bài hát (Song) trong Database.
Nhiệm vụ: Khai báo các cột thông tin bài hát (tiêu đề, ca sĩ, đường dẫn file, thời lượng...).
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from src.database.db import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    genre = Column(String(50), nullable=True, default=None)       # The loai CHINH - AI hoc va phan loai
    sub_genres = Column(String(200), nullable=True, default=None) # Tags phu - chi hien thi UI
    filepath = Column(String(500), nullable=False)
    duration = Column(Float, default=0.0)
    has_features = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
