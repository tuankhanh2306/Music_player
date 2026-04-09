"""
File: src/config.py
Chức năng: Quản lý cấu hình toàn cục của ứng dụng.
Nhiệm vụ: Đọc các biến môi trường từ file .env (Database URL, thư mục upload, cài đặt AI) và cung cấp thông qua object `settings`.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    UPLOAD_DIR: str = "uploads"
    FEATURE_CACHE_PATH: str = "data/features.npy"
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_AUDIO_EXTENSIONS: List[str] = [".mp3", ".wav", ".flac"]

    # Validator tự động chặt chuỗi cách nhau bằng dấu phẩy thành List
    @field_validator("ALLOWED_AUDIO_EXTENSIONS", mode="before")
    @classmethod
    def parse_audio_extensions(cls, v):
        if isinstance(v, str):
            import json
            try:
                # Thử parse JSON nếu là dạng [".mp3", ...]
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except:
                pass
            return [ext.strip() for ext in v.split(",") if ext.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()