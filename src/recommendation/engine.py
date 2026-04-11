import logging
from typing import List

import numpy as np

from src.audio_processing.feature_extraction import load_feature_cache
from src.core.exceptions import ModelNotFittedException, SongNotFoundException
from src.recommendation.knn_model import fit_knn, load_model, save_model

logger = logging.getLogger(__name__)


def get_similar_songs(target_song_id: int, top_k: int = 5) -> List[int]:
    """Return top_k song IDs most similar to target_song_id.

    Raises:
        ModelNotFittedException: If the model hasn't been trained yet.
        SongNotFoundException: If target_song_id has no features in the cache.
    """
    try:
        model, song_ids = load_model()
    except ModelNotFittedException:
        logger.warning("get_similar_songs called but model is not fitted.")
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
    """Rebuild and persist the KNN model from the current feature cache."""
    cache = load_feature_cache()

    if len(cache) < 2:
        logger.warning(
            "retrain_model skipped: only %d song(s) in cache (minimum 2 required).", len(cache)
        )
        return

    song_ids = list(cache.keys())
    features_matrix = np.array([cache[sid] for sid in song_ids])

    model = fit_knn(features_matrix, song_ids)
    save_model(model, song_ids)
    logger.info("KNN model retrained with %d songs.", len(song_ids))
