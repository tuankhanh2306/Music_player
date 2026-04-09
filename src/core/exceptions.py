from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class SongNotFoundException(Exception):
    def __init__(self, message="Không tìm thấy bài hát yêu cầu."):
        self.message = message
        super().__init__(self.message)

class InvalidAudioFileException(Exception):
    def __init__(self, message="Định dạng file không hợp lệ hoặc file bị lỗi."):
        self.message = message
        super().__init__(self.message)

class FeatureExtractionException(Exception):
    def __init__(self, message="Lỗi trong quá trình trích xuất đặc trưng âm thanh."):
        self.message = message
        super().__init__(self.message)

class ModelNotFittedException(Exception):
    def __init__(self, message="Hệ thống gợi ý chưa sẵn sàng (chưa được huấn luyện)."):
        self.message = message
        super().__init__(self.message)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(SongNotFoundException)
    async def song_not_found_handler(request: Request, exc: SongNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"error": "SongNotFound", "detail": exc.message}
        )
        
    @app.exception_handler(InvalidAudioFileException)
    async def invalid_audio_file_handler(request: Request, exc: InvalidAudioFileException):
        return JSONResponse(
            status_code=400,
            content={"error": "InvalidAudioFile", "detail": exc.message}
        )
        
    @app.exception_handler(FeatureExtractionException)
    async def feature_extraction_handler(request: Request, exc: FeatureExtractionException):
        return JSONResponse(
            status_code=500,
            content={"error": "FeatureExtractionError", "detail": exc.message}
        )
        
    @app.exception_handler(ModelNotFittedException)
    async def model_not_fitted_handler(request: Request, exc: ModelNotFittedException):
        return JSONResponse(
            status_code=503,
            content={"error": "ModelNotFitted", "detail": exc.message}
        )
