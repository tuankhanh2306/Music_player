from sqlalchemy.orm import Session
from src.database import crud
from src.core.exceptions import SongNotFoundException

def create_new_playlist(db: Session, name: str):
    return crud.create_playlist(db, name=name)

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
