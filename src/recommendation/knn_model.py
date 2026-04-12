import logging
import os
import pickle
from typing import List, Tuple

import numpy as np
from sklearn.neighbors import NearestNeighbors

from src.core.exceptions import ModelNotFittedException

logger = logging.getLogger(__name__)

DEFAULT_MODEL_PATH = "data/knn_model.pkl"


def fit_knn(features_matrix: np.ndarray, song_ids: List[int]) -> NearestNeighbors:
    """Huấn luyện mô hình KNN với ma trận đặc trưng đầu vào.

    Args:
        features_matrix: Mảng 2 chiều có dạng (số_bài_hát, số_đặc_trưng).
        song_ids: Danh sách ID bài hát theo đúng thứ tự với các dòng trong features_matrix.

    Returns:
        Đối tượng NearestNeighbors đã được huấn luyện.
    """
    try:
        n_neighbors = min(6, len(song_ids))
        model = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine", algorithm="brute")
        model.fit(features_matrix)
        logger.info("KNN đã được huấn luyện với %d bài hát (n_neighbors=%d)", len(song_ids), n_neighbors)
        return model
    except Exception as exc:
        logger.error("fit_knn bị lỗi: %s", exc)
        raise


def save_model(
    model: NearestNeighbors,
    song_ids: List[int],
    model_path: str = DEFAULT_MODEL_PATH,
) -> None:
    """Lưu mô hình đã huấn luyện và danh sách song_id xuống file."""
    try:
        os.makedirs(os.path.dirname(model_path) if os.path.dirname(model_path) else ".", exist_ok=True)
        with open(model_path, "wb") as f:
            pickle.dump((model, song_ids), f)
        logger.info("Đã lưu mô hình KNN vào '%s'", model_path)
    except Exception as exc:
        logger.error("save_model bị lỗi: %s", exc)
        raise


def load_model(model_path: str = DEFAULT_MODEL_PATH) -> Tuple[NearestNeighbors, List[int]]:
    """Tải mô hình KNN từ file.

    Returns:
        Tuple gồm (mô hình NearestNeighbors đã huấn luyện, danh sách song_ids theo thứ tự).

    Raises:
        ModelNotFittedException: Nếu file mô hình không tồn tại.
    """
    if not os.path.exists(model_path):
        raise ModelNotFittedException()
    try:
        with open(model_path, "rb") as f:
            model, song_ids = pickle.load(f)
        logger.info("Đã tải mô hình KNN từ '%s' (%d bài hát)", model_path, len(song_ids))
        return model, song_ids
    except ModelNotFittedException:
        raise
    except Exception as exc:
        logger.error("load_model bị lỗi: %s", exc)
        raise ModelNotFittedException() from exc