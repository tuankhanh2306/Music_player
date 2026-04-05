# 📋 AI Agent Task Breakdown: AI Music Player
**Status:** In Progress
**Project Type:** 100% Python (FastAPI, Librosa, Scikit-learn, SQLAlchemy)

---
## 🤖 [INSTRUCTION FOR AI AGENTS]
- When assigned a task from this file, read the "Dependencies" first.
- Strictly follow the target file paths and function signatures.
- Use Mock Data if the dependent track is not yet completed.
- Update the `[ ]` to `[x]` when a task is fully tested and completed.

---

## 👤 TRACK 1: DATABASE & STORAGE (Data Engineer)
**Goal:** Setup SQLite and SQLAlchemy ORM.
**Dependencies:** None. Independent track.

- [ ] **Task 1.1: Database Configuration**
  - **File:** `src/database/db.py`
  - **Logic:** Initialize SQLAlchemy `engine`, `SessionLocal`, and `Base` class for MySQL (`mysql+pymysql://root:password@localhost:3306/music_db` - loaded from `.env`). Provide a `get_db()` generator for FastAPI dependency injection.
- [ ] **Task 1.2: Define Models**
  - **File:** `src/models/` (create `song.py`, `user.py`, `playlist.py`)
  - **Logic:** - `Song`: id (int), title (str), artist (str), filepath (str), duration (float).
    - `Playlist`: id (int), name (str).
    - Create a Many-to-Many relationship table `playlist_song`.
- [ ] **Task 1.3: CRUD Operations**
  - **File:** `src/database/crud.py`
  - **Signatures:**
    - `def create_song(db: Session, title: str, artist: str, filepath: str) -> Song:`
    - `def get_song(db: Session, song_id: int) -> Song:`
    - `def get_all_songs(db: Session) -> List[Song]:`
- [ ] **Task 1.4: Mock Data Seeder**
  - **File:** `src/seed_data.py`
  - **Logic:** Write a script that creates all tables (`Base.metadata.create_all`) and inserts 5 dummy songs into the database.

---

## 👤 TRACK 2: BACKEND API (Backend Engineer)
**Goal:** Create RESTful APIs using FastAPI.
**Dependencies:** Track 1 (Database) for models. Use mock responses if Track 3 & 4 are not ready.

- [ ] **Task 2.1: Server Initialization**
  - **File:** `src/main.py`
  - **Logic:** Initialize `FastAPI()`. Add CORS Middleware to allow all origins `["*"]`. Include routers from `api/`.
- [ ] **Task 2.2: Song Upload Route**
  - **File:** `src/api/song_routes.py`
  - **Signature:** `async def upload_song(file: UploadFile = File(...), db: Session = Depends(get_db)):`
  - **Logic:** Save `file` to `uploads/` folder. Call `crud.create_song()` to save to DB. Return `{"song_id": id, "status": "success"}`.
- [ ] **Task 2.3: Audio Streaming Route**
  - **File:** `src/api/song_routes.py`
  - **Signature:** `def stream_audio(song_id: int, db: Session = Depends(get_db)):`
  - **Logic:** Query DB for `filepath`. Return FastAPI `FileResponse(filepath, media_type="audio/mpeg")`.
- [ ] **Task 2.4: Recommendation Route (Mock Phase)**
  - **File:** `src/api/recommend_routes.py`
  - **Signature:** `def get_recommendations(song_id: int):`
  - **Logic:** Temporarily return hardcoded JSON: `{"target_song": song_id, "recommended_ids": [2, 3, 5]}`.

---

## 👤 TRACK 3: AUDIO PROCESSING (Data Scientist)
**Goal:** Extract MFCC features from audio files using `librosa`.
**Dependencies:** Local `.mp3` files in `uploads/` folder for testing.

- [ ] **Task 3.1: MFCC Extraction Function**
  - **File:** `src/audio_processing/feature_extraction.py`
  - **Signature:** `def extract_mfcc(file_path: str, n_mfcc: int = 20) -> np.ndarray:`
  - **Logic:** - Use `librosa.load(file_path, sr=22050)`.
    - Use `librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)`.
    - Apply `np.mean(mfcc, axis=1)` to flatten the 2D array into a 1D vector of shape `(20,)`.
- [ ] **Task 3.2: Batch Processing & Caching**
  - **File:** `src/audio_processing/feature_extraction.py`
  - **Signature:** `def update_feature_cache(song_id: int, mfcc_vector: np.ndarray, cache_path: str = "data/features.npy"):`
  - **Logic:** Load existing `.npy` dictionary, append the new `{song_id: vector}`, and save it back to disk.

---

## 👤 TRACK 4: AI RECOMMENDATION (ML Engineer)
**Goal:** Compute similarities and return nearest neighbors.
**Dependencies:** `data/features.npy` from Track 3. (Use Mock Numpy array if not ready).

- [ ] **Task 4.1: KNN Model Setup**
  - **File:** `src/recommendation/knn_model.py`
  - **Signature:** `def fit_knn(features_matrix: np.ndarray):`
  - **Logic:** Initialize `NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')` from `sklearn`. Fit the model with `features_matrix`.
- [ ] **Task 4.2: Recommendation Engine**
  - **File:** `src/recommendation/engine.py`
  - **Signature:** `def get_similar_songs(target_song_id: int, top_k: int = 5) -> List[int]:`
  - **Logic:** 1. Load `data/features.npy`.
    2. Extract vector for `target_song_id`.
    3. Pass vector to KNN model.
    4. Return a list of nearest `song_id`s (excluding the target song itself).

---

## 👤 TRACK 5: FRONTEND UI (Frontend Engineer)
**Goal:** Simple UI to upload, play, and show recommendations.
**Dependencies:** Track 2 API endpoints. (Use Postman mock server if APIs are down).

- [ ] **Task 5.1: HTML Structure**
  - **File:** `src/frontend/index.html` (or `templates/index.html`)
  - **Logic:** Create a simple layout: Upload Form, `<audio id="player">` element, and a `<ul>` list for Recommendations. Use CDN Bootstrap/Tailwind.
- [ ] **Task 5.2: JS Fetch Audio**
  - **File:** `src/frontend/app.js`
  - **Logic:** Fetch `GET /songs`, list them. When clicked, change the `<audio src="...">` to `http://localhost:8000/songs/{id}`.
- [ ] **Task 5.3: JS Fetch AI Recommendation**
  - **File:** `src/frontend/app.js`
  - **Logic:** Listen to the `play` event of the audio player. Extract the current playing `song_id`, call `GET /recommend/{song_id}`. Parse JSON and render the result list on the UI.

---
## 🚀 INTEGRATION (Tech Lead)
- [ ] **Task 6.1:** Connect `extract_mfcc` (Track 3) into the `upload_song` route (Track 2).
- [ ] **Task 6.2:** Connect `get_similar_songs` (Track 4) into the `get_recommendations` route (Track 2).