"""
File: main.py
Chức năng: Điểm khởi đầu của ứng dụng (Entry point).
Nhiệm vụ: Khởi tạo FastAPI app, cấu hình Middleware (CORS), đăng ký các Router API và Exception Handlers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Các import khác sẽ được thêm khi làm Track 3
app = FastAPI(title="AI Music Player API")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Music Player API v2.1 (No-Auth)"}
