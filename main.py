from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.song_routes import router as song_router
from src.api.playlist_routes import router as playlist_router
from src.api.recommend_routes import router as recommend_router
from src.core.exceptions import setup_exception_handlers
from src.core.logger import setup_logging

# Khởi tạo Logger
setup_logging()

app = FastAPI(
    title="AI Music Player API",
    version="2.1",
    description="Backend API for AI Music Player - No-Auth Version"
)

# Đăng ký Exception Handlers
setup_exception_handlers(app)

# Config CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký Routers
app.include_router(song_router)
app.include_router(playlist_router)
app.include_router(recommend_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Music Player API v2.1 (No-Auth) is running!"}
