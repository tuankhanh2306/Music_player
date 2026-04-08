from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema dùng khi User đăng ký (nhận password gốc)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema dùng khi trả thông tin User về (giấu password)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True # Bắt buộc để Pydantic đọc được data từ SQLAlchemy Model