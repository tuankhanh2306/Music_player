"""
Script: backfill_features.py
Chức năng: Trích xuất MFCC cho tất cả bài hát có has_features=False,
           cập nhật cache .npy, và retrain KNN model + Genre Classifier.
Chạy: python backfill_features.py
"""
import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

from src.database.db import SessionLocal
from src.database.crud import get_all_songs, update_song_feature_status
from src.audio_processing.feature_extraction import extract_mfcc, update_feature_cache
from src.recommendation.engine import retrain_model

def backfill():
    db = SessionLocal()
    try:
        songs = get_all_songs(db, limit=1000)
        pending = [s for s in songs if not s.has_features]

        if not pending:
            logger.info("✅ Tất cả bài hát đã có features. Không cần backfill.")
            return

        logger.info(f"📋 Tìm thấy {len(pending)}/{len(songs)} bài chưa có features. Bắt đầu trích xuất...")

        success_count = 0
        fail_count    = 0

        for i, song in enumerate(pending, 1):
            filepath = song.filepath

            # Thử đường dẫn tuyệt đối và tương đối
            if not os.path.exists(filepath):
                abs_path = os.path.join(os.path.dirname(__file__), filepath)
                if os.path.exists(abs_path):
                    filepath = abs_path
                else:
                    logger.warning(f"[{i}/{len(pending)}] ❌ File không tồn tại: {song.filepath} — bỏ qua.")
                    fail_count += 1
                    continue

            logger.info(f"[{i}/{len(pending)}] 🎵 Đang xử lý: [{song.id}] {song.artist} – {song.title}")
            try:
                mfcc_vector = extract_mfcc(filepath)
                update_feature_cache(song.id, mfcc_vector)
                update_song_feature_status(db, song.id, has_features=True)
                logger.info(f"             ✅ Thành công! Vector shape: {mfcc_vector.shape}")
                success_count += 1
            except Exception as e:
                logger.error(f"             ❌ Lỗi trích xuất MFCC: {e}")
                fail_count += 1

        # Retrain cả 2 model sau khi xong
        logger.info("\n🤖 Đang retrain KNN Model + Genre Classifier...")
        retrain_model()

        logger.info(f"\n{'='*50}")
        logger.info(f"🎉 BACKFILL HOÀN TẤT!")
        logger.info(f"   ✅ Thành công : {success_count} bài")
        logger.info(f"   ❌ Thất bại   : {fail_count} bài")
        logger.info(f"{'='*50}")

    except Exception as e:
        logger.error(f"❌ Lỗi backfill: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    backfill()
