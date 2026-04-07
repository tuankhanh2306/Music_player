from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    UPLOAD_DIR: str = "uploads"
    FEATURE_CACHE_PATH: str = "data/features.npy"
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_AUDIO_EXTENSIONS: List[str] = [".mp3", ".wav", ".flac"]

    # Validator tự động chặt chuỗi cách nhau bằng dấu phẩy thành List
    @field_validator("ALLOWED_AUDIO_EXTENSIONS", mode="before")
    @classmethod
    def parse_audio_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",") if ext.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()