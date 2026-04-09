# 📋 AI Agent Task Breakdown: AI Music Player

**Status:** In Progress
**Project Type:** 100% Python (FastAPI, Librosa, Scikit-learn, SQLAlchemy)
**Version:** 2.1 — No Authentication

---

## 🤖 Instruction for AI Agents

- **Đọc phần Dependencies trước** khi bắt tay vào bất kỳ task nào.
- **Tuân thủ tuyệt đối** file path và function signature được chỉ định.
- **Dùng Mock Data** nếu track phụ thuộc chưa hoàn thành.
- **Cập nhật trạng thái** `[ ]` → `[x]` chỉ khi task đã pass toàn bộ test case liên quan.
- **Definition of Done (DoD):** Một task được coi là DONE khi: code chạy không lỗi, có unit test cover case chính, và đã được review bởi ít nhất 1 người khác.
- **Error Handling:** Mọi function phải có try/except và raise lỗi có ý nghĩa. Không để exception trần lan ra ngoài.
- **Convention log:** Dùng `logger = logging.getLogger(__name__)` tại mỗi module. Không dùng `print()` trong production code.

---

## 📐 Kiến Trúc Tổng Quan

```
Request → Router → Service Layer → [CRUD / Audio / ML] → Response
                       ↓
                 Error Handler (HTTPException)
                       ↓
                   Logger (ghi log lỗi)
```

Mọi business logic **phải đi qua Service Layer**, không được gọi thẳng từ Router sang CRUD hay ML functions. Không có Auth middleware — tất cả endpoints đều public.

---

## 📁 Cấu Trúc Thư Mục

```text
ai_music_player/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── alembic.ini
├── alembic/
│   └── versions/
├── main.py
├── src/
│   ├── config.py
│   ├── api/
│   │   ├── song_routes.py
│   │   ├── playlist_routes.py
│   │   └── recommend_routes.py
│   ├── services/
│   │   ├── song_service.py
│   │   ├── playlist_service.py
│   │   └── recommend_service.py
│   ├── audio_processing/
│   │   └── feature_extraction.py
│   ├── recommendation/
│   │   ├── knn_model.py
│   │   └── engine.py
│   ├── database/
│   │   ├── db.py
│   │   └── crud.py
│   ├── models/
│   │   ├── song.py
│   │   └── playlist.py
│   ├── schemas/
│   │   ├── song_schema.py
│   │   └── playlist_schema.py
│   └── core/
│       ├── exceptions.py
│       └── logger.py
├── tests/
│   ├── unit/
│   │   ├── test_feature_extraction.py
│   │   ├── test_knn_model.py
│   │   └── test_crud.py
│   └── integration/
│       ├── test_upload_flow.py
│       └── test_recommend_flow.py
├── uploads/
├── data/
└── docs/
    └── api_spec.md
```

> **Lưu ý:** So với v2.0, các file sau đã bị loại bỏ hoàn toàn:
> `src/models/user.py` · `src/schemas/user_schema.py` · `src/core/security.py` · `src/api/auth_routes.py` · `src/services/auth_service.py`

---

## Track 0 — Project Setup & Configuration

**Goal:** Khởi tạo môi trường dự án chuẩn trước khi các track khác bắt đầu.
**Dependencies:** Không có. Phải hoàn thành **trước tất cả** các track khác.

- [x] **Task 0.1 — Khởi tạo cấu trúc thư mục và Git**
  - Tạo toàn bộ cấu trúc thư mục như trên.
  - Tạo file `.gitignore` bao gồm: `__pycache__/`, `*.pyc`, `.env`, `uploads/`, `data/`, `*.npy`.
  - Khởi tạo git repository.

- [x] **Task 0.2 — Quản lý Dependencies**

  File: `requirements.txt`

  ```
  fastapi==0.111.0
  uvicorn[standard]==0.30.0
  sqlalchemy==2.0.30
  alembic==1.13.1
  pymysql==1.1.1
  python-dotenv==1.0.1
  python-multipart==0.0.9
  librosa==0.10.2
  scikit-learn==1.5.0
  numpy==1.26.4
  filelock==3.14.0
  pytest==8.2.0
  httpx==0.27.0
  ```

  > So với v2.0, đã bỏ: `python-jose[cryptography]`, `passlib[bcrypt]`.

- [x] **Task 0.3 — Environment Configuration**

  File: `.env.example`

  ```env
  # Database
  DATABASE_URL=mysql+pymysql://root:password@localhost:3306/music_db

  # App
  UPLOAD_DIR=uploads
  FEATURE_CACHE_PATH=data/features.npy
  MAX_UPLOAD_SIZE_MB=50
  ALLOWED_AUDIO_EXTENSIONS=.mp3,.wav,.flac
  ```

  > So với v2.0, đã bỏ: `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`.

- [x] **Task 0.4 — Centralized Config**

  File: `src/config.py`

  ```python
  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      DATABASE_URL: str
      UPLOAD_DIR: str = "uploads"
      FEATURE_CACHE_PATH: str = "data/features.npy"
      MAX_UPLOAD_SIZE_MB: int = 50
      ALLOWED_AUDIO_EXTENSIONS: list[str] = [".mp3", ".wav", ".flac"]

      class Config:
          env_file = ".env"

  settings = Settings()
  ```

- [x] **Task 0.5 — Logger Setup**

  File: `src/core/logger.py`

  Logic: Config `logging` module với format chuẩn (timestamp, level, module, message). Output ra console và file `logs/app.log`.

- [x] **Task 0.6 — Custom Exceptions**

  File: `src/core/exceptions.py`

  ```python
  class SongNotFoundException(Exception): ...
  class InvalidAudioFileException(Exception): ...
  class FeatureExtractionException(Exception): ...
  class ModelNotFittedException(Exception): ...
  ```

  Handler: Đăng ký `@app.exception_handler` để trả về JSON chuẩn `{"error": "...", "detail": "..."}` thay vì HTTP 500 trần.

---

## Track 1 — Database & Storage

**Goal:** Setup MySQL và SQLAlchemy ORM với migration support.
**Dependencies:** Task 0.4 phải hoàn thành trước.

- [ ] **Task 1.1 — Database Configuration**

  File: `src/database/db.py`

  ```python
  def get_db() -> Generator[Session, None, None]:
  ```

  Logic:
  - Khởi tạo `engine` từ `settings.DATABASE_URL` (không hardcode).
  - Config connection pool: `pool_size=10`, `max_overflow=20`, `pool_pre_ping=True`.
  - Cung cấp `SessionLocal` và `get_db()` generator cho FastAPI dependency injection.
  - Tạo thư mục `uploads/` và `data/` nếu chưa tồn tại.

- [ ] **Task 1.2 — Alembic Migration Setup**

  Logic:
  - Chạy `alembic init alembic`.
  - Cập nhật `alembic/env.py` để import `Base` từ models và dùng `settings.DATABASE_URL`.
  - Tạo migration đầu tiên: `alembic revision --autogenerate -m "initial_tables"`.
  - Áp dụng: `alembic upgrade head`.

  > Không dùng `Base.metadata.create_all()` trong production.

- [ ] **Task 1.3 — Define Models**

  **`Song`** — file: `src/models/song.py`
  ```
  id (int, PK)
  title (str)
  artist (str)
  filepath (str)
  duration (float)
  has_features (bool, default=False)
  created_at (datetime)
  ```

  **`Playlist`** — file: `src/models/playlist.py`
  ```
  id (int, PK)
  name (str)
  created_at (datetime)
  ```

  **`playlist_song`** (Association Table)
  ```
  playlist_id (FK → Playlist.id)
  song_id (FK → Song.id)
  added_at (datetime)
  ```

  > So với v2.0: không có `User` model, không có `uploaded_by` trong `Song`, không có `owner_id` trong `Playlist`.

- [ ] **Task 1.4 — Pydantic Schemas**

  File: `src/schemas/song_schema.py`

  ```python
  class SongCreate(BaseModel):
      title: str
      artist: str

  class SongResponse(BaseModel):
      id: int
      title: str
      artist: str
      duration: float
      has_features: bool
      created_at: datetime

      class Config:
          from_attributes = True

  class SongUpdate(BaseModel):
      title: str | None = None
      artist: str | None = None
  ```

  File: `src/schemas/playlist_schema.py` — tương tự, không có `owner_id`.

- [ ] **Task 1.5 — CRUD Operations**

  File: `src/database/crud.py`

  ```python
  def create_song(db: Session, title: str, artist: str, filepath: str) -> Song:
  def get_song(db: Session, song_id: int) -> Song | None:
  def get_all_songs(db: Session, skip: int = 0, limit: int = 100) -> List[Song]:
  def update_song_feature_status(db: Session, song_id: int, has_features: bool) -> Song:
  def create_playlist(db: Session, name: str) -> Playlist:
  def add_song_to_playlist(db: Session, playlist_id: int, song_id: int) -> None:
  def get_playlist_songs(db: Session, playlist_id: int) -> List[Song]:
  ```

  Lưu ý: Mỗi hàm phải commit và refresh object trước khi return. Không để exception trần.

- [ ] **Task 1.6 — Mock Data Seeder**

  File: `src/seed_data.py`

  Logic: Chạy Alembic migration → insert 5 dummy songs → tạo 1 playlist mẫu với 3 bài trong đó. Chạy được bằng `python src/seed_data.py`.

---

## Track 2 — Authentication

> **Track này đã bị loại bỏ hoàn toàn.**
>
> Tất cả API endpoints là public. Không cần JWT, không cần login, không cần `Authorization` header. Bỏ qua toàn bộ track này và tiếp tục từ Track 3.

---

## Track 3 — Backend API

**Goal:** Tạo RESTful APIs bằng FastAPI với đầy đủ validation.
**Dependencies:** Track 1 (Database). Dùng mock responses nếu Track 4 & 5 chưa sẵn sàng.

- [ ] **Task 3.1 — Server Initialization**

  File: `main.py`

  Logic:
  - Khởi tạo `FastAPI()` với `title`, `version`, `description`.
  - Đăng ký CORS Middleware (chỉ allow origin cụ thể trong production).
  - Đăng ký tất cả custom exception handlers từ `src/core/exceptions.py`.
  - Include routers: `song_routes`, `playlist_routes`, `recommend_routes`.
  - Thêm `startup` event: fit KNN model nếu `data/features.npy` đã tồn tại.

- [ ] **Task 3.2 — Song Upload Route**

  File: `src/api/song_routes.py`
  Endpoint: `POST /songs/upload`

  ```python
  async def upload_song(
      file: UploadFile = File(...),
      title: str = Form(...),
      artist: str = Form(...),
      db: Session = Depends(get_db),
  ) -> SongResponse:
  ```

  Logic (delegate sang `song_service.py`):
  1. Validate extension `.mp3/.wav/.flac` và file size ≤ `settings.MAX_UPLOAD_SIZE_MB`.
  2. Sanitize filename dùng `pathlib` + `uuid` để tránh path traversal.
  3. Lưu file vào `uploads/`.
  4. Lưu metadata vào DB qua `crud.create_song()`.
  5. Trả về `SongResponse`.

- [ ] **Task 3.3 — Song Service**

  File: `src/services/song_service.py`

  ```python
  async def process_upload(db: Session, file: UploadFile, title: str, artist: str) -> Song:
  def get_song_or_404(db: Session, song_id: int) -> Song:
  def get_all_songs(db: Session) -> List[Song]:
  ```

- [ ] **Task 3.4 — Audio Streaming Route**

  File: `src/api/song_routes.py`
  Endpoint: `GET /songs/{song_id}/stream`

  ```python
  def stream_audio(
      song_id: int,
      db: Session = Depends(get_db),
  ) -> FileResponse:
  ```

  Logic: Query DB lấy `filepath`. Kiểm tra file tồn tại trên disk. Raise `HTTP 404` nếu không có. Return `FileResponse(filepath, media_type="audio/mpeg")`.

- [ ] **Task 3.5 — List Songs Route**

  File: `src/api/song_routes.py`
  Endpoint: `GET /songs`

  Trả về danh sách tất cả bài hát. Hỗ trợ `skip` và `limit` pagination.

- [ ] **Task 3.6 — Playlist Routes**

  File: `src/api/playlist_routes.py`

  - `POST /playlists` — Tạo playlist mới.
  - `POST /playlists/{playlist_id}/songs` — Thêm bài hát vào playlist.
  - `GET /playlists/{playlist_id}/songs` — Lấy danh sách bài hát trong playlist.

- [ ] **Task 3.7 — Recommendation Route (Mock Phase)**

  File: `src/api/recommend_routes.py`
  Endpoint: `GET /recommend/{song_id}`

  ```python
  def get_recommendations(
      song_id: int,
      top_k: int = 5,
      db: Session = Depends(get_db),
  ) -> dict:
  ```

  Logic (Mock): Trả về hardcoded JSON `{"target_song": song_id, "recommended_ids": [2, 3, 5]}`. Sẽ được thay thế ở Task 7.2.

---

## Track 4 — Audio Processing

**Goal:** Trích xuất đặc trưng MFCC từ file audio và cache an toàn.
**Dependencies:** Task 0.3 (Config), Task 0.5 (Logger). File `.mp3` trong `uploads/` để test.

- [ ] **Task 4.1 — MFCC Extraction Function**

  File: `src/audio_processing/feature_extraction.py`

  ```python
  def extract_mfcc(file_path: str, n_mfcc: int = 20) -> np.ndarray:
  ```

  Logic:
  - Validate `file_path` tồn tại, raise `FileNotFoundError` nếu không có.
  - Dùng `librosa.load(file_path, sr=22050)`.
  - Dùng `librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)`.
  - Apply `np.mean(mfcc, axis=1)` → vector `(n_mfcc,)`.
  - Wrap trong try/except, raise `FeatureExtractionException` nếu librosa lỗi.
  - Log thời gian xử lý.

- [ ] **Task 4.2 — Thread-Safe Feature Cache**

  File: `src/audio_processing/feature_extraction.py`

  ```python
  def update_feature_cache(song_id: int, mfcc_vector: np.ndarray, cache_path: str = None) -> None:
  def load_feature_cache(cache_path: str = None) -> dict[int, np.ndarray]:
  ```

  Logic (Thread-Safe):
  - Dùng `filelock.FileLock(cache_path + ".lock")` để lock file trước khi đọc/ghi.
  - `load_feature_cache`: Load file `.npy` (`allow_pickle=True`). Nếu không tồn tại, trả về dict rỗng.
  - `update_feature_cache`: Load cache → thêm `{song_id: vector}` → save lại. Toàn bộ trong lock block.
  - `cache_path` mặc định lấy từ `settings.FEATURE_CACHE_PATH`.

- [ ] **Task 4.3 — Unit Tests cho Audio Processing**

  File: `tests/unit/test_feature_extraction.py`

  Test cases:
  - `test_extract_mfcc_output_shape` — Đảm bảo output shape là `(20,)`.
  - `test_extract_mfcc_invalid_path` — Đảm bảo raise đúng exception khi file không tồn tại.
  - `test_update_feature_cache_concurrent` — 5 thread cùng ghi cache, đảm bảo không mất data.

---

## Track 5 — AI Recommendation

**Goal:** Xây dựng recommendation engine dùng KNN.
**Dependencies:** `data/features.npy` từ Track 4. Dùng Mock numpy array nếu chưa có.

- [ ] **Task 5.1 — KNN Model**

  File: `src/recommendation/knn_model.py`

  ```python
  def fit_knn(features_matrix: np.ndarray, song_ids: List[int]) -> NearestNeighbors:
  def save_model(model: NearestNeighbors, song_ids: List[int], model_path: str = "data/knn_model.pkl") -> None:
  def load_model(model_path: str = "data/knn_model.pkl") -> tuple[NearestNeighbors, List[int]]:
  ```

  Logic:
  - `fit_knn`: Khởi tạo `NearestNeighbors(n_neighbors=6, metric='cosine', algorithm='brute')`. Fit với `features_matrix`. Lưu `song_ids` map theo thứ tự hàng trong matrix.
  - `save_model`: Dùng `pickle` để lưu `(model, song_ids)` vào disk.
  - `load_model`: Load từ disk. Raise `ModelNotFittedException` nếu file không tồn tại.

  > Model state phải được persist ra disk — server restart sẽ mất RAM.

- [ ] **Task 5.2 — Recommendation Engine**

  File: `src/recommendation/engine.py`

  ```python
  def get_similar_songs(target_song_id: int, top_k: int = 5) -> List[int]:
  def retrain_model() -> None:
  ```

  Logic `get_similar_songs`:
  1. Load model từ disk. Nếu fail → raise `ModelNotFittedException`.
  2. Load cache từ `load_feature_cache()`.
  3. Kiểm tra `target_song_id` có trong cache. Nếu không → raise `SongNotFoundException`.
  4. Lấy vector của `target_song_id`. Query KNN với `n_neighbors = top_k + 1`.
  5. Lọc bỏ `target_song_id` khỏi kết quả. Trả về `top_k` song IDs gần nhất.

  Logic `retrain_model`:
  1. Load toàn bộ cache.
  2. Kiểm tra có ít nhất 2 bài hát. Nếu không → log warning và return.
  3. Build `features_matrix` và `song_ids` list từ cache dict.
  4. Gọi `fit_knn()` → `save_model()`.
  5. Log số lượng bài hát đã train.

- [ ] **Task 5.3 — Unit Tests cho Recommendation**

  File: `tests/unit/test_knn_model.py`

  Test cases:
  - `test_fit_knn_returns_model` — Đảm bảo trả về model đã fit.
  - `test_get_similar_songs_excludes_target` — Đảm bảo target_song_id không có trong kết quả.
  - `test_get_similar_songs_song_not_in_cache` — Đảm bảo raise đúng exception.
  - `test_get_similar_songs_model_not_fitted` — Đảm bảo raise đúng exception khi chưa có model file.

---

## Track 6 — Frontend UI

**Goal:** Giao diện web đơn giản để upload, phát nhạc và xem gợi ý.
**Dependencies:** Track 3 API endpoints. Dùng Postman mock server nếu API chưa sẵn sàng.

- [ ] **Task 6.1 — HTML Structure**

  File: `src/frontend/index.html`

  Layout gồm:
  - Form upload nhạc (title, artist, file).
  - Danh sách bài hát (`<ul id="song-list">`).
  - Player (`<audio id="player" controls>`).
  - Panel gợi ý (`<ul id="recommendation-list">`).

  Dùng CDN Tailwind CSS cho styling.

  > So với v2.0: đã bỏ form đăng nhập / đăng ký.

- [ ] **Task 6.2 — JS - API Request Helper**

  File: `src/frontend/app.js`

  Logic:
  - Tạo helper function `apiRequest(url, options)` để wrap các lần gọi API.
  - Không cần header `Authorization`.
  - Nếu API trả về lỗi (4xx / 5xx), hiển thị thông báo lỗi thân thiện cho người dùng.

  > So với v2.0: đã bỏ toàn bộ phần JWT, sessionStorage, và redirect về login.

- [ ] **Task 6.3 — JS - Song List & Playback**

  File: `src/frontend/app.js`

  Logic:
  - Gọi `GET /songs` để render danh sách khi trang load.
  - Khi click vào bài hát → set `audio.src = /songs/{id}/stream`.
  - Lưu `currentSongId` vào state.

- [ ] **Task 6.4 — JS - AI Recommendation**

  File: `src/frontend/app.js`

  Logic:
  - Lắng nghe event `play` của audio player.
  - Lấy `currentSongId`, gọi `GET /recommend/{song_id}`.
  - Parse JSON, render danh sách gợi ý. Mỗi item có thể click để phát.
  - Hiển thị loading spinner khi đang chờ API.
  - Hiển thị thông báo lỗi thân thiện nếu API thất bại.

---

## Track 7 — Integration & Testing

**Goal:** Kết nối toàn bộ pipeline và đảm bảo hệ thống hoạt động end-to-end.
**Dependencies:** Tất cả các Track từ 1, 3, 4, 5 phải hoàn thành.

- [ ] **Task 7.1 — Kết nối Audio Processing vào Upload Flow**

  File: `src/services/song_service.py`

  Logic — sau khi lưu file và DB thành công trong `process_upload()`:
  1. Gọi `extract_mfcc(filepath)` trong một try/except riêng.
  2. Nếu thành công: gọi `update_feature_cache()`, gọi `crud.update_song_feature_status(has_features=True)`.
  3. Nếu thất bại: Log lỗi, **không** raise exception (upload vẫn thành công).
  4. **Tùy chọn nâng cao:** Chạy extract MFCC trong `BackgroundTasks` của FastAPI để không block response.

- [ ] **Task 7.2 — Kết nối Recommendation Engine vào API**

  File: `src/services/recommend_service.py`

  ```python
  def get_recommendations_for_song(db: Session, song_id: int, top_k: int = 5) -> dict:
  ```

  Logic:
  1. Kiểm tra song tồn tại trong DB (raise `HTTP 404` nếu không).
  2. Kiểm tra `has_features = True`. Nếu không → trả về `{"message": "Bài hát chưa được xử lý features", "recommended_ids": []}`.
  3. Gọi `engine.get_similar_songs(song_id, top_k)`.
  4. Bắt `ModelNotFittedException` → trả về thông báo hữu ích.
  5. Trả về `{"target_song": song_id, "recommended_ids": [...]}`.

- [ ] **Task 7.3 — Retrain Trigger**

  Logic: Sau mỗi lần `update_feature_cache()` thành công trong Task 7.1, gọi `engine.retrain_model()` trong background. Đảm bảo model luôn up-to-date sau mỗi lần upload.

- [ ] **Task 7.4 — Integration Tests**

  File: `tests/integration/test_upload_flow.py`, `tests/integration/test_recommend_flow.py`

  Test cases:
  - `test_full_upload_flow` — Upload file → check DB có record → check `data/features.npy` có entry.
  - `test_full_recommend_flow` — Upload 3 file → gọi recommend → nhận về list không rỗng, không chứa target song.
  - `test_recommend_before_upload` — Gọi recommend khi chưa có bài hát → nhận lỗi thân thiện.

- [ ] **Task 7.5 — API Documentation Review**

  File: `docs/api_spec.md`

  Logic: Review FastAPI auto-generated Swagger tại `/docs`. Bổ sung description, example request/response cho từng endpoint. Viết README hướng dẫn cài đặt và chạy project từ đầu.

---

## 📊 Dependency Graph

```
Track 0 (Setup)
    ↓
Track 1 (Database) ←────── Track 0
    ↓
Track 3 (API) ←──────────── Track 1
    ↓
Track 4 (Audio) ←────────── Track 0
Track 5 (ML) ←───────────── Track 4
    ↓
Track 7 (Integration) ←──── Track 3 + Track 4 + Track 5
    ↓
Track 6 (Frontend) ←─────── Track 3
```

---

## 📋 Checklist Tổng Quan

| Track | Mô tả | Số Task | Status |
|-------|-------|---------|--------|
| Track 0 | Project Setup | 6 | ⬜ |
| Track 1 | Database & Storage | 6 | ⬜ |
| ~~Track 2~~ | ~~Authentication~~ | ~~4~~ | ❌ Đã xóa |
| Track 3 | Backend API | 7 | ⬜ |
| Track 4 | Audio Processing | 3 | ⬜ |
| Track 5 | AI Recommendation | 3 | ⬜ |
| Track 6 | Frontend UI | 4 | ⬜ |
| Track 7 | Integration & Testing | 5 | ⬜ |
| **Tổng** | | **34** | |

---

## ⚠️ Nguyên Tắc Không Được Vi Phạm

1. **Không hardcode** credentials, secret key, hay connection string trong code. Tất cả phải qua `.env`.
2. **Không dùng `print()`** trong production code. Chỉ dùng `logger`.
3. **Không ghi đồng thời vào `features.npy`** mà không có file lock.
4. **Không commit file `.env`** lên git.
5. **Không để exception trần (`bare except`)** lan ra response. Phải catch và trả về HTTP error code phù hợp.
6. **Không retrain KNN** trong main request thread — phải chạy background.