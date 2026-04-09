from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from src.models.song import Song
from src.models.playlist import Playlist
import logging

logger = logging.getLogger(__name__)

# ================= SONG CRUD =================
def create_song(db: Session, title: str, artist: str, filepath: str) -> Song:
    try:
        db_song = Song(title=title, artist=artist, filepath=filepath)
        db.add(db_song)
        db.commit()
        db.refresh(db_song)
        return db_song
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating song: {e}")
        raise

def get_song(db: Session, song_id: int) -> Song | None:
    return db.query(Song).filter(Song.id == song_id).first()

def get_all_songs(db: Session, skip: int = 0, limit: int = 100) -> List[Song]:
    return db.query(Song).offset(skip).limit(limit).all()

def update_song_feature_status(db: Session, song_id: int, has_features: bool) -> Song | None:
    song = get_song(db, song_id)
    if song:
        try:
            song.has_features = has_features
            db.commit()
            db.refresh(song)
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while updating song feature status: {e}")
            raise
    return song

# ================= PLAYLIST CRUD =================
def create_playlist(db: Session, name: str) -> Playlist:
    try:
        db_playlist = Playlist(name=name)
        db.add(db_playlist)
        db.commit()
        db.refresh(db_playlist)
        return db_playlist
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating playlist: {e}")
        raise

def add_song_to_playlist(db: Session, playlist_id: int, song_id: int) -> None:
    try:
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        song = get_song(db, song_id)
        
        # Chỉ thêm nếu playlist và song tồn tại, và bài hát chưa có trong playlist
        if playlist and song and song not in playlist.songs:
            playlist.songs.append(song)
            db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while adding song to playlist: {e}")
        raise

def get_playlist_songs(db: Session, playlist_id: int) -> List[Song]:
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    return playlist.songs if playlist else []