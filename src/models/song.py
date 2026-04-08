from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from src.database.db import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    duration = Column(Float, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    has_features = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())