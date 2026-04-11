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
    """Fit a KNN model on the given feature matrix.

    Args:
        features_matrix: 2-D array of shape (n_songs, n_features).
        song_ids: Ordered list of song IDs matching rows in features_matrix.

    Returns:
        Fitted NearestNeighbors instance.
    """
    try:
        n_neighbors = min(6, len(song_ids))
        model = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine", algorithm="brute")
        model.fit(features_matrix)
        logger.info("KNN fitted on %d songs (n_neighbors=%d)", len(song_ids), n_neighbors)
        return model
    except Exception as exc:
        logger.error("fit_knn failed: %s", exc)
        raise


def save_model(
    model: NearestNeighbors,
    song_ids: List[int],
    model_path: str = DEFAULT_MODEL_PATH,
) -> None:
    """Persist the fitted model and its song_id mapping to disk."""
    try:
        os.makedirs(os.path.dirname(model_path) if os.path.dirname(model_path) else ".", exist_ok=True)
        with open(model_path, "wb") as f:
            pickle.dump((model, song_ids), f)
        logger.info("KNN model saved to '%s'", model_path)
    except Exception as exc:
        logger.error("save_model failed: %s", exc)
        raise


def load_model(model_path: str = DEFAULT_MODEL_PATH) -> Tuple[NearestNeighbors, List[int]]:
    """Load the KNN model from disk.

    Returns:
        Tuple of (fitted NearestNeighbors, ordered list of song_ids).

    Raises:
        ModelNotFittedException: If the model file does not exist.
    """
    if not os.path.exists(model_path):
        raise ModelNotFittedException()
    try:
        with open(model_path, "rb") as f:
            model, song_ids = pickle.load(f)
        logger.info("KNN model loaded from '%s' (%d songs)", model_path, len(song_ids))
        return model, song_ids
    except ModelNotFittedException:
        raise
    except Exception as exc:
        logger.error("load_model failed: %s", exc)
        raise ModelNotFittedException() from exc
