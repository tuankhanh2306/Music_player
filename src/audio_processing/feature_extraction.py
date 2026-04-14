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
    Trích xuất đặc trưng âm thanh kết hợp:
    - MFCC (20 chiều): Độ rung/âm sắc.
    - Tempo (1 chiều): Vận tốc BPM (cực kỳ quan trọng để tách EDM và Ballad).
    - Spectral Centroid (1 chiều): Độ "sáng" của âm thanh (tiếng tress, synth chói).
    - Zero Crossing Rate (1 chiều): Độ "nhiễu/gắt" của âm thanh (Snare, Hi-hat).
    Tổng cộng: 23 chiều.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")

    start_time = time.time()
    
    try:
        y, sr = librosa.load(file_path, sr=22050)
        
        # 1. Trích xuất MFCC (20 chiều)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        mfcc_vector = np.mean(mfcc, axis=1) # Shape: (20,)
        
        # 2. Trích xuất Tempo (BPM) (1 chiều)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo_val = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
        
        # 3. Trích xuất Spectral Centroid (1 chiều)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        centroid_val = float(np.mean(centroid))
        
        # 4. Trích xuất Zero Crossing Rate (1 chiều)
        zcr = librosa.feature.zero_crossing_rate(y=y)
        zcr_val = float(np.mean(zcr))
        
        # 5. Gộp tất cả lại thành 1 vector duy nhất (23 chiều)
        # Các giá trị này có thang đo rất khác nhau (Beat: 120, Centroid: 2000, ZCR: 0.1)
        # Sẽ cần StandardScaler ở bước huấn luyện mô hình (engine.py)
        combined_vector = np.hstack((mfcc_vector, [tempo_val, centroid_val, zcr_val]))
        
        process_time = time.time() - start_time
        logger.info(f"Đã trích xuất 23-dim features cho '{os.path.basename(file_path)}' trong {process_time:.2f}s")
        
        return combined_vector
        
    except Exception as e:
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

def remove_song_from_cache(song_id: int, cache_path: str = None) -> None:
    """
    Xoá vector đặc trưng của song_id khỏi file cache (.npy) nếu có.
    """
    path = cache_path or settings.FEATURE_CACHE_PATH
    lock_path = path + ".lock"

    if not os.path.exists(path):
        return

    with FileLock(lock_path):
        try:
            cache = np.load(path, allow_pickle=True).item()
        except Exception:
            cache = {}
        
        if song_id in cache:
            del cache[song_id]
            np.save(path, cache)
            logger.info(f"Đã xoá vector đặc trưng của song_id={song_id} khỏi cache.")    