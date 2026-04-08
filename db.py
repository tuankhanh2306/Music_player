import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from src.config import settings

# Tạo thư mục uploads/ và data/ nếu chưa tồn tại
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
# Vì FEATURE_CACHE_PATH chứa cả tên file (VD: data/features.npy), ta cần lấy thư mục chứa nó
os.makedirs(os.path.dirname(settings.FEATURE_CACHE_PATH), exist_ok=True)

# Khởi tạo engine từ settings (không hardcode) với connection pool
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