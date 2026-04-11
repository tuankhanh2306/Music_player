import logging
from typing import List

import numpy as np

from src.audio_processing.feature_extraction import load_feature_cache
from src.core.exceptions import ModelNotFittedException, SongNotFoundException
from src.recommendation.knn_model import fit_knn, load_model, save_model

logger = logging.getLogger(__name__)


def get_similar_songs(target_song_id: int, top_k: int = 5) -> List[int]:
    """Trả về top_k ID bài hát có độ tương đồng cao nhất với target_song_id.

    Raises:
        ModelNotFittedException: Nếu mô hình chưa được huấn luyện.
        SongNotFoundException: Nếu target_song_id không có trong cache đặc trưng.
    """
    try:
        model, song_ids = load_model()
    except ModelNotFittedException:
        logger.warning("get_similar_songs được gọi nhưng mô hình chưa được huấn luyện.")
        raise

    cache = load_feature_cache()

    if target_song_id not in cache:
        raise SongNotFoundException(target_song_id)

    target_vector = cache[target_song_id].reshape(1, -1)

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


def retrain_model() -> None:
    """Huấn luyện lại và lưu mô hình KNN từ cache đặc trưng hiện tại."""
    cache = load_feature_cache()

    if len(cache) < 2:
        logger.warning(
            "retrain_model bị bỏ qua: chỉ có %d bài hát trong cache (tối thiểu cần 2).", len(cache)
        )
        return

    song_ids = list(cache.keys())
    features_matrix = np.array([cache[sid] for sid in song_ids])

    model = fit_knn(features_matrix, song_ids)
    save_model(model, song_ids)
    logger.info("Đã huấn luyện lại mô hình KNN với %d bài hát.", len(song_ids))