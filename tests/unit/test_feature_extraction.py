import os
import pytest
import numpy as np
import tempfile
import threading
from unittest.mock import patch
from src.audio_processing.feature_extraction import (
    extract_mfcc,
    update_feature_cache,
    load_feature_cache,
    FeatureExtractionException
)

# ==============================================================
# 1. Test đảm bảo output shape là (20,)
# ==============================================================
@patch('os.path.exists')
@patch('librosa.load')
@patch('librosa.feature.mfcc')
def test_extract_mfcc_output_shape(mock_mfcc, mock_load, mock_exists):
    # Giả lập file tồn tại để không bị vướng vòng Validate
    mock_exists.return_value = True
    
    # Giả lập librosa load file thành công (trả về y và sr)
    mock_load.return_value = (np.zeros(22050), 22050)
    
    # Giả lập MFCC trả về ma trận 2D có shape (20, 100) - 20 n_mfcc, 100 frames
    mock_mfcc.return_value = np.random.rand(20, 100)
    
    # Chạy hàm
    result = extract_mfcc("dummy_audio.mp3", n_mfcc=20)
    
    # Hàm np.mean(axis=1) bên trong extract_mfcc sẽ gom (20, 100) thành vector 1D (20,)
    assert result.shape == (20,), f"Shape mong đợi (20,) nhưng nhận được {result.shape}"

# ==============================================================
# 2. Test raise đúng Exception khi file không tồn tại
# ==============================================================
def test_extract_mfcc_invalid_path():
    # Bắt lỗi FileNotFoundError bằng pytest
    with pytest.raises(FileNotFoundError) as excinfo:
        extract_mfcc("duong_dan_ao_khong_ton_tai.mp3")
    
    assert "không tồn tại" in str(excinfo.value)

# ==============================================================
# 3. Test Thread-Safe: 5 thread cùng ghi cache không mất data
# ==============================================================
def test_update_feature_cache_concurrent():
    # Dùng thư mục tạm của hệ điều hành để không làm rác project thật
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_path = os.path.join(temp_dir, "test_features.npy")
        
        # Hàm worker mà mỗi luồng sẽ chạy
        def worker(song_id):
            # Tạo một vector giả đặc trưng cho từng bài hát (vd: bài 0 full số 0, bài 1 full số 1...)
            fake_vector = np.full((20,), song_id, dtype=float)
            update_feature_cache(song_id, fake_vector, cache_path=cache_path)

        threads = []
        num_threads = 5
        
        # Tạo và khởi chạy 5 luồng cùng lúc
        for i in range(num_threads):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
            
        # Bắt main thread đợi cho 5 luồng con chạy xong hết
        for t in threads:
            t.join()
            
        # Đọc lại file cache xem data có nguyên vẹn không
        final_cache = load_feature_cache(cache_path)
        
        # Kiểm tra: Phải có đủ 5 bài hát
        assert len(final_cache) == num_threads, f"Kỳ vọng 5 bài hát nhưng chỉ lưu được {len(final_cache)}"
        
        # Kiểm tra: Dữ liệu của từng bài hát không bị đè nhầm lên nhau
        for i in range(num_threads):
            assert i in final_cache, f"Thiếu dữ liệu của song_id {i}"
            assert np.array_equal(final_cache[i], np.full((20,), i, dtype=float))
