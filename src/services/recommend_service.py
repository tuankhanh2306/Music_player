import logging
from sqlalchemy.orm import Session
from typing import List

from src.database import crud
from src.recommendation import engine
from src.core.exceptions import SongNotFoundException, ModelNotFittedException

logger = logging.getLogger(__name__)

def get_recommendations_for_song(db: Session, song_id: int, top_k: int = 5) -> List[int]:
    """
    Kết nối Engine AI để trả về các bài hát tương tự.
    """
    # 1. Kiểm tra bài hát có tồn tại không
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    
    # 2. Kiểm tra trạng thái features
    if not song.has_features:
        logger.warning(f"Bài hát {song_id} chưa được trích xuất đặc trưng.")
        return []

    # 3. Gọi engine lấy danh sách ID
    try:
        recommend_ids = engine.get_similar_songs(song_id, top_k=top_k)
        return recommend_ids
    except ModelNotFittedException:
        logger.error("Mô hình KNN chưa được huấn luyện.")
        raise
    except Exception as e:
        logger.error(f"Lỗi khi lấy gợi ý cho bài hát {song_id}: {e}")
        return []


def build_ai_radio(db: Session, seed_song_id: int, queue_size: int = 20) -> List[int]:
    """
    Tạo danh sách phát AI Radio từ một bài hát "mồi" (seed).

    Thuật toán:
    1. Bắt đầu từ seed_song_id.
    2. Lặp: lấy top_k bài tương tự nhất của bài hiện tại (KNN).
    3. Chọn bài chưa xuất hiện trong hàng chờ → thêm vào queue.
    4. Bài tiếp theo để tìm tương tự = bài vừa thêm (chaining).
    5. Dừng khi đủ queue_size hoặc không còn bài mới nào.

    Kết quả: [seed_id, song_A, song_B, song_C, ...] — list phát liên tục.
    """
    # Validate seed song
    seed = crud.get_song(db, seed_song_id)
    if not seed:
        raise SongNotFoundException()
    if not seed.has_features:
        raise ValueError(f"Bài hát seed ({seed_song_id}) chưa được trích xuất đặc trưng MFCC.")

    visited: set = {seed_song_id}
    queue: List[int] = [seed_song_id]
    current_id = seed_song_id

    # Số bài còn cần thêm vào queue
    remaining = queue_size - 1

    while remaining > 0:
        try:
            # Lấy top_k bài tương tự với bài hiện tại
            # Lấy dư để có đủ bài chưa visited
            fetch_k = min(remaining + 5, 10)
            similars = engine.get_similar_songs(current_id, top_k=fetch_k)
        except (ModelNotFittedException, SongNotFoundException) as e:
            logger.warning(f"AI Radio: không thể lấy gợi ý từ song_id={current_id}: {e}")
            break

        # Lọc bài chưa có trong queue
        new_songs = [sid for sid in similars if sid not in visited]

        if not new_songs:
            # Không tìm được bài mới nào → thử fallback: lấy tất cả bài có features
            logger.info(f"AI Radio: chain đứt tại song_id={current_id}, thử fallback...")
            all_songs = crud.get_all_songs(db, limit=500)
            fallback = [
                s.id for s in all_songs
                if s.has_features and s.id not in visited
            ]
            if not fallback:
                logger.info("AI Radio: không còn bài nào để thêm.")
                break
            # Chọn bài đầu tiên của fallback (bài gần nhất theo ID)
            new_songs = fallback[:1]

        # Thêm các bài mới vào queue (tối đa đủ remaining)
        for sid in new_songs:
            if remaining <= 0:
                break
            queue.append(sid)
            visited.add(sid)
            remaining -= 1
            current_id = sid  # Chaining: bài tiếp theo dùng bài vừa thêm

    logger.info(
        f"AI Radio built: seed={seed_song_id}, queue_size={len(queue)}, "
        f"IDs={queue}"
    )
    return queue
