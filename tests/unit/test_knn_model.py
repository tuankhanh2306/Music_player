"""Unit tests for KNN recommendation model (Track 5)."""
import os

import numpy as np
import pytest



@pytest.fixture()
def sample_cache(tmp_path, monkeypatch):
    """Populate a feature cache with 5 synthetic songs and patch settings."""
    from src.audio_processing.feature_extraction import update_feature_cache
    from src import config as cfg_module

    cache_path = str(tmp_path / "features.npy")
    monkeypatch.setattr(cfg_module.settings, "FEATURE_CACHE_PATH", cache_path)

    np.random.seed(42)
    for song_id in range(1, 6):
        update_feature_cache(song_id, np.random.rand(20), cache_path=cache_path)

    return cache_path


@pytest.fixture()
def fitted_model(sample_cache, tmp_path):
    from src.audio_processing.feature_extraction import load_feature_cache
    from src.recommendation.knn_model import fit_knn, save_model

    model_path = str(tmp_path / "knn_model.pkl")
    cache = load_feature_cache(sample_cache)
    song_ids = list(cache.keys())
    matrix = np.array([cache[sid] for sid in song_ids])
    model = fit_knn(matrix, song_ids)
    save_model(model, song_ids, model_path=model_path)
    return model_path, song_ids


class TestFitKnn:
    def test_fit_knn_returns_model(self, sample_cache):
        from src.audio_processing.feature_extraction import load_feature_cache
        from src.recommendation.knn_model import fit_knn

        cache = load_feature_cache(sample_cache)
        song_ids = list(cache.keys())
        matrix = np.array([cache[sid] for sid in song_ids])
        model = fit_knn(matrix, song_ids)
        # Model should expose kneighbors
        assert hasattr(model, "kneighbors")

class TestGetSimilarSongs:
    def test_get_similar_songs_excludes_target(self, fitted_model, monkeypatch, sample_cache):
        from src import config as cfg_module
        from src.recommendation import engine

        model_path, song_ids = fitted_model
        monkeypatch.setattr(cfg_module.settings, "FEATURE_CACHE_PATH", sample_cache)

        # Patch load_model to use our temp path
        from src.recommendation import knn_model
        monkeypatch.setattr(knn_model, "DEFAULT_MODEL_PATH", model_path)

        target = song_ids[0]
        results = engine.get_similar_songs(target, top_k=3)
        assert target not in results, "Target song must not appear in recommendations."
        assert len(results) <= 3

    def test_get_similar_songs_song_not_in_cache(self, fitted_model, monkeypatch, sample_cache):
        from src import config as cfg_module
        from src.core.exceptions import SongNotFoundException
        from src.recommendation import engine, knn_model

        model_path, _ = fitted_model
        monkeypatch.setattr(cfg_module.settings, "FEATURE_CACHE_PATH", sample_cache)
        monkeypatch.setattr(knn_model, "DEFAULT_MODEL_PATH", model_path)

        with pytest.raises(SongNotFoundException):
            engine.get_similar_songs(9999, top_k=3)

    def test_get_similar_songs_model_not_fitted(self, tmp_path, monkeypatch, sample_cache):
        from src import config as cfg_module
        from src.core.exceptions import ModelNotFittedException
        from src.recommendation import engine, knn_model

        monkeypatch.setattr(cfg_module.settings, "FEATURE_CACHE_PATH", sample_cache)
        monkeypatch.setattr(knn_model, "DEFAULT_MODEL_PATH", str(tmp_path / "no_model.pkl"))

        with pytest.raises(ModelNotFittedException):
            engine.get_similar_songs(1, top_k=3)
