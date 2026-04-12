from sqlalchemy.orm import Session
from src.database import crud
from src.core.exceptions import SongNotFoundException

def create_new_playlist(db: Session, name: str):
    return crud.create_playlist(db, name=name)

def create_smart_playlist(db: Session, song_id: int, limit: int = 10, name: str | None = None):
    # 1. Kiểm tra bài hát gốc
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    
    # 2. Sinh tên nếu không có
    playlist_name = name or f"Radio: {song.title}"
    
    # 3. Lấy bài hát tương tự từ AI Model
    from src.recommendation.engine import get_similar_songs
    try:
        similar_ids = get_similar_songs(song_id, top_k=limit)
    except Exception:
        similar_ids = []
        
    # Tạo danh sách ID các bài được add (gồm bài gốc + các bài tương tự)
    track_ids = [song_id] + similar_ids
    
    # 4. Tạo playlist mới
    new_playlist = crud.create_playlist(db, name=playlist_name)
    
    # 5. Thêm tất cả các bài hát vào playlist vừa tạo
    for tid in track_ids:
        # ignore missing songs for safety
        if crud.get_song(db, tid):
            crud.add_song_to_playlist(db, new_playlist.id, tid)
            
    # Lấy lại playlist đầy đủ cùng list songs
    return new_playlist

def add_song(db: Session, playlist_id: int, song_id: int):
    # Kiểm tra song có tồn tại không
    song = crud.get_song(db, song_id)
    if not song:
        raise SongNotFoundException()
    
    # Ở phiên bản No-Auth, ta không check owner_id
    crud.add_song_to_playlist(db, playlist_id, song_id)
    return {"message": "Đã thêm bài hát vào playlist thành công."}

def get_songs(db: Session, playlist_id: int):
    return crud.get_playlist_songs(db, playlist_id)

def get_all_playlists(db: Session):
    return crud.get_all_playlists(db)

def remove_song(db: Session, playlist_id: int, song_id: int):
    success = crud.remove_song_from_playlist(db, playlist_id, song_id)
    if not success:
        return {"message": "Playlist hoặc bài hát không tồn tại."}
    return {"message": "Đã xóa bài hát khỏi playlist thành công."}

def delete_playlist(db: Session, playlist_id: int):
    success = crud.delete_playlist(db, playlist_id)
    if not success:
        return {"message": "Playlist không tồn tại."}
    return {"message": "Đã xóa playlist thành công."}
