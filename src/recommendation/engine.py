import logging
from typing import List, Optional, Tuple

import numpy as np

from src.audio_processing.feature_extraction import load_feature_cache
from src.core.exceptions import ModelNotFittedException, SongNotFoundException
from src.recommendation.knn_model import (
    fit_knn, load_model, save_model,
    fit_genre_classifier, save_genre_classifier, load_genre_classifier
)

logger = logging.getLogger(__name__)


def get_similar_songs(target_song_id: int, top_k: int = 5) -> List[int]:
    """Trả về top_k ID bài hát có độ tương đồng cao nhất với target_song_id.

    Raises:
        ModelNotFittedException: Nếu mô hình chưa được huấn luyện.
        SongNotFoundException: Nếu target_song_id không có trong cache đặc trưng.
    """
    try:
        model, scaler, song_ids = load_model()
    except ModelNotFittedException:
        logger.warning("get_similar_songs được gọi nhưng mô hình chưa được huấn luyện.")
        raise

    cache = load_feature_cache()

    if target_song_id not in cache:
        raise SongNotFoundException(target_song_id)

    target_vector = cache[target_song_id].reshape(1, -1)
    # Scale feature_vector bằng scaler đã huấn luyện
    target_vector = scaler.transform(target_vector)

    n_neighbors = min(top_k + 1, len(song_ids))
    distances, indices = model.kneighbors(target_vector, n_neighbors=n_neighbors)

    similar_ids = []
    for idx in indices[0]:
        sid = song_ids[idx]
        if sid != target_song_id:
            similar_ids.append(sid)
        if len(similar_ids) >= top_k:
            break

    logger.info(
        "get_similar_songs: target=%d top_k=%d results=%s",
        target_song_id, top_k, similar_ids,
    )
    return similar_ids


def predict_genre(song_id: int) -> Optional[str]:
    """
    Dự đoán thể loại bài hát dựa trên vector MFCC và Genre Classifier.
    Trả về None nếu classifier chưa được huấn luyện hoặc bài không có đặc trưng.
    """
    clf = load_genre_classifier()
    if clf is None:
        logger.info("predict_genre: Genre Classifier chưa tồn tại (cần nhiều bài có nhãn hơn).")
        return None

    cache = load_feature_cache()
    if song_id not in cache:
        logger.warning("predict_genre: song_id=%d chưa có vector MFCC.", song_id)
        return None

    vector = cache[song_id].reshape(1, -1)
    try:
        predicted = clf.predict(vector)
        genre = predicted[0]
        logger.info("predict_genre: song_id=%d -> '%s'", song_id, genre)
        return genre
    except Exception as e:
        logger.error("predict_genre lỗi: %s", e)
        return None

def predict_genre_with_confidence(feature_vector: np.ndarray) -> Tuple[Optional[str], float]:
    """
    Dự đoán thể loại bài hát nhận từ vector ngẫu nhiên (chưa lưu DB) kèm theo độ tin cậy (%).
    Sử dụng predict_proba để tính tỷ lệ bầu chọn Majority Voting.
    """
    clf = load_genre_classifier()
    if clf is None:
        logger.info("predict_genre: Genre Classifier chưa tồn tại.")
        return None, 0.0

    vector = feature_vector.reshape(1, -1)
    try:
        # Dự đoán nhãn
        predicted = clf.predict(vector)
        genre = predicted[0]
        
        # Dự đoán xác suất
        proba = clf.predict_proba(vector)
        confidence = float(np.max(proba)) * 100
        
        logger.info("predict_genre_with_confidence: -> '%s' (%.1f%%)", genre, confidence)
        return genre, confidence
    except Exception as e:
        logger.error("predict_genre_with_confidence lỗi: %s", e)
        return None, 0.0

def retrain_model() -> None:
    """Huấn luyện lại và lưu cả 2 mô hình: KNN Similarity và Genre Classifier."""
    cache = load_feature_cache()

    if len(cache) < 2:
        logger.warning(
            "retrain_model bị bỏ qua: chỉ có %d bài hát trong cache (tối thiểu cần 2).", len(cache)
        )
        return

    song_ids = list(cache.keys())
    features_matrix = np.array([cache[sid] for sid in song_ids])

    # 1. Huấn luyện KNN Similarity (để gợi ý nhạc tương tự)
    model, scaler = fit_knn(features_matrix, song_ids)
    save_model(model, scaler, song_ids)
    logger.info("Đã huấn luyện lại mô hình KNN với %d bài hát.", len(song_ids))

    # 2. Huấn luyện Genre Classifier (chỉ khi có bài hát có nhãn genre)
    try:
        from src.database.db import SessionLocal
        from src.database.crud import get_all_songs
        db = SessionLocal()
        all_songs = get_all_songs(db)
        db.close()

        # Lọc ra những bài có genre và có vector trong cache
        labeled_ids = [s.id for s in all_songs if s.genre and s.id in cache]
        labeled_genres = [s.genre for s in all_songs if s.genre and s.id in cache]

        if len(labeled_ids) >= 2:
            labeled_matrix = np.array([cache[sid] for sid in labeled_ids])
            clf = fit_genre_classifier(labeled_matrix, labeled_ids, labeled_genres)
            if clf is not None:
                save_genre_classifier(clf)
                logger.info("Đã huấn luyện Genre Classifier với %d bài có nhãn.", len(labeled_ids))
        else:
            logger.info("Genre Classifier chưa huấn luyện: cần ít nhất 2 bài có nhãn genre (hiện có %d).", len(labeled_ids))
    except Exception as e:
        logger.warning("Không thể huấn luyện Genre Classifier: %s", e)
