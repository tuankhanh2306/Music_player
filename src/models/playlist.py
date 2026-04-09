"""
File: src/models/playlist.py
Chức năng: Định nghĩa cấu trúc bảng Playlist và mối quan hệ với Song.
Nhiệm vụ: Chứa thông tin playlist và bảng trung gian `playlist_song` (nhiều-nhiều).
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.db import Base

# Association table for Many-to-Many relationship between Playlist and Song
playlist_song = Table(
    'playlist_song',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id', ondelete="CASCADE"), primary_key=True),
    Column('song_id', Integer, ForeignKey('songs.id', ondelete="CASCADE"), primary_key=True),
    Column('added_at', DateTime(timezone=True), server_default=func.now())
)

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Many-to-Many relationship with Song
    songs = relationship("Song", secondary=playlist_song, backref="playlists")
