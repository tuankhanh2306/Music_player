"""
File: src/database/db.py
Chức năng: Thiết lập kết nối cơ sở dữ liệu (Database Connection).
Nhiệm vụ: Tạo SQLAlchemy Engine, SessionLocal để làm việc với DB và cung cấp Dependency `get_db` cho FastAPI.
"""
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from src.config import settings

# Tạo thư mục uploads/ và data/ nếu chưa tồn tại
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.FEATURE_CACHE_PATH), exist_ok=True)

# Khởi tạo engine từ settings. 
# Cho SQLite, ta cần connect_args={"check_same_thread": False} cho FastAPI.
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )

# Cung cấp SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Generator cho FastAPI dependency injection
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
