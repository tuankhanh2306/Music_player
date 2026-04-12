import logging
import os
import pickle
from typing import List, Tuple, Optional, Dict

import numpy as np
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier

from src.core.exceptions import ModelNotFittedException

logger = logging.getLogger(__name__)

DEFAULT_MODEL_PATH = "data/knn_model.pkl"
DEFAULT_CLASSIFIER_PATH = "data/genre_classifier.pkl"


def fit_knn(features_matrix: np.ndarray, song_ids: List[int]) -> NearestNeighbors:
    """Huấn luyện mô hình KNN Similarity Search (để gợi ý bài hát tương tự)."""
    try:
        n_neighbors = min(6, len(song_ids))
        model = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine", algorithm="brute")
        model.fit(features_matrix)
        logger.info("KNN đã được huấn luyện với %d bài hát (n_neighbors=%d)", len(song_ids), n_neighbors)
        return model
    except Exception as exc:
        logger.error("fit_knn bị lỗi: %s", exc)
        raise


def fit_genre_classifier(
    features_matrix: np.ndarray, 
    song_ids: List[int], 
    genre_labels: List[str]
) -> Optional[KNeighborsClassifier]:
    """
    Huấn luyện mô hình KNN Classifier (để phân loại thể loại mới).
    Chỉ huấn luyện nếu có ít nhất 2 thể loại khác nhau trong dữ liệu.
    """
    if len(set(genre_labels)) < 2:
        logger.warning("Genre Classifier bị bỏ qua: cần ít nhất 2 thể loại khác nhau (hiện có %d).", len(set(genre_labels)))
        return None
    try:
        n_neighbors = min(5, len(song_ids))
        clf = KNeighborsClassifier(n_neighbors=n_neighbors, metric="cosine", algorithm="brute")
        clf.fit(features_matrix, genre_labels)
        logger.info("Genre Classifier đã huấn luyện với %d bài / %d thể loại", 
                    len(song_ids), len(set(genre_labels)))
        return clf
    except Exception as exc:
        logger.error("fit_genre_classifier bị lỗi: %s", exc)
        return None


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


def save_genre_classifier(
    clf: KNeighborsClassifier,
    classifier_path: str = DEFAULT_CLASSIFIER_PATH,
) -> None:
    """Lưu Genre Classifier xuống file."""
    try:
        os.makedirs(os.path.dirname(classifier_path) if os.path.dirname(classifier_path) else ".", exist_ok=True)
        with open(classifier_path, "wb") as f:
            pickle.dump(clf, f)
        logger.info("Đã lưu Genre Classifier vào '%s'", classifier_path)
    except Exception as exc:
        logger.error("save_genre_classifier bị lỗi: %s", exc)


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


def load_genre_classifier(classifier_path: str = DEFAULT_CLASSIFIER_PATH) -> Optional[KNeighborsClassifier]:
    """Tải Genre Classifier từ file. Trả về None nếu chưa tồn tại."""
    if not os.path.exists(classifier_path):
        return None
    try:
        with open(classifier_path, "rb") as f:
            clf = pickle.load(f)
        logger.info("Đã tải Genre Classifier từ '%s'", classifier_path)
        return clf
    except Exception as exc:
        logger.error("load_genre_classifier bị lỗi: %s", exc)
        return None