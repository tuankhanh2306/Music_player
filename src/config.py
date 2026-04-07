from pydantic_settings import BaseSettings, SettingsConfigDict
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

    # Dùng pydantic-settings kết hợp với python-dotenv để load từ .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
