import os
import time
import librosa
import numpy as np
import logging
from filelock import FileLock
from src.config import settings

# Setup logger cơ bản (sẽ dùng cấu hình từ Task 0.5 của nhóm nếu có)
logger = logging.getLogger(__name__)

# Định nghĩa Custom Exception như yêu cầu
class FeatureExtractionException(Exception):
    pass

def extract_mfcc(file_path: str, n_mfcc: int = 20) -> np.ndarray:
    """
    Trích xuất đặc trưng MFCC từ file audio.
    """
    # 1. Validate file_path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")

    start_time = time.time()
    
    try:
        # 2. Dùng librosa load file với sample rate 22050
        y, sr = librosa.load(file_path, sr=22050)
        
        # 3. Trích xuất MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        
        # 4. Apply np.mean để lấy vector 1 chiều
        mfcc_vector = np.mean(mfcc, axis=1)
        
        # 6. Log thời gian xử lý
        process_time = time.time() - start_time
        logger.info(f"Đã trích xuất MFCC cho '{os.path.basename(file_path)}' trong {process_time:.2f}s")
        
        return mfcc_vector
        
    except Exception as e:
        # 5. Wrap trong try/except và raise custom exception
        logger.error(f"Lỗi librosa khi xử lý {file_path}: {str(e)}")
        raise FeatureExtractionException(f"Lỗi trích xuất đặc trưng: {str(e)}")

def load_feature_cache(cache_path: str = None) -> dict[int, np.ndarray]:
    """
    Load cache chứa vector đặc trưng (MFCC) của các bài hát.
    Sử dụng FileLock để đảm bảo an toàn khi đọc/ghi đa luồng.
    """
    path = cache_path or settings.FEATURE_CACHE_PATH
    lock_path = path + ".lock"
    
    # Đảm bảo thư mục chứa file cache đã tồn tại
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Khoá file lại trước khi đọc
    with FileLock(lock_path):
        if not os.path.exists(path):
            return {}
        try:
            # np.load trả về một mảng 0 chiều chứa dict, dùng .item() để lấy dict ra
            cache = np.load(path, allow_pickle=True).item()
            return cache
        except Exception as e:
            logger.error(f"Lỗi khi đọc file cache {path}: {str(e)}")
            return {}

def update_feature_cache(song_id: int, mfcc_vector: np.ndarray, cache_path: str = None) -> None:
    """
    Cập nhật vector mới vào cache và lưu xuống file (.npy).
    Toàn bộ quá trình Đọc -> Thêm -> Ghi đều nằm trong Lock Block.
    """
    path = cache_path or settings.FEATURE_CACHE_PATH
    lock_path = path + ".lock"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Khoá file lại trong suốt quá trình Đọc - Sửa - Ghi
    with FileLock(lock_path):
        # 1. Đọc cache cũ lên
        if os.path.exists(path):
            try:
                cache = np.load(path, allow_pickle=True).item()
            except Exception:
                cache = {}
        else:
            cache = {}
            
        # 2. Thêm dữ liệu mới
        cache[song_id] = mfcc_vector
        
        # 3. Ghi đè xuống file
        np.save(path, cache)
        logger.info(f"Đã lưu vector đặc trưng của song_id={song_id} vào cache.")    