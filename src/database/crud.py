"""
File: src/database/crud.py
Chức năng: Thực hiện các thao tác CRUD (Create, Read, Update, Delete) cơ bản.
Nhiệm vụ: Chứa các hàm tương tác trực tiếp với Database thông qua SQLAlchemy (Thêm bài hát, lấy playlist, ...).
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from src.models.song import Song
from src.models.playlist import Playlist
import logging

logger = logging.getLogger(__name__)

# ================= SONG CRUD =================
def create_song(db: Session, title: str, artist: str, filepath: str, genre: str | None = None, sub_genres: str | None = None, duration: float = 0.0) -> Song:
    try:
        db_song = Song(title=title, artist=artist, filepath=filepath, genre=genre, sub_genres=sub_genres, duration=duration)
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

def update_song_metadata(db: Session, song_id: int, title: str | None = None, artist: str | None = None, genre: str | None = None, sub_genres: str | None = None) -> Song | None:
    song = get_song(db, song_id)
    if song:
        try:
            if title is not None:
                song.title = title
            if artist is not None:
                song.artist = artist
            if genre is not None:
                song.genre = genre
            if sub_genres is not None:
                song.sub_genres = sub_genres
            db.commit()
            db.refresh(song)
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while updating song metadata: {e}")
            raise
    return song

def delete_song(db: Session, song_id: int) -> bool:
    song = get_song(db, song_id)
    if song:
        try:
            db.delete(song)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while deleting song: {e}")
            raise
    return False

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

def get_all_playlists(db: Session) -> List[Playlist]:
    return db.query(Playlist).all()

def remove_song_from_playlist(db: Session, playlist_id: int, song_id: int) -> bool:
    try:
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        song = get_song(db, song_id)
        
        if playlist and song and song in playlist.songs:
            playlist.songs.remove(song)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while removing song from playlist: {e}")
        raise

def delete_playlist(db: Session, playlist_id: int) -> bool:
    try:
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if playlist:
            db.delete(playlist)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while deleting playlist: {e}")
        raise

