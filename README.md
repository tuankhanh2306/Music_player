# 🎵 AI Music Player

> Một hệ thống trình phát nhạc thông minh, xây dựng hoàn toàn bằng Python. Dự án tích hợp AI để tự động phân tích âm thanh, phân loại thể loại nhạc bằng KNN, gợi ý bài hát tương đồng qua MFCC, và tự động tạo lời bài hát qua OpenAI Whisper.

## 📑 Mục lục

- [Tính năng](#-tính-năng)
- [Công nghệ sử dụng](#️-công-nghệ-sử-dụng)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Các lưu ý quan trọng](#-các-lưu-ý-quan-trọng)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Tính năng

| Tính năng | Mô tả |
|---|---|
| 🎧 **Phát nhạc** | Upload và stream file MP3/WAV/FLAC qua API |
| 📋 **Quản lý Playlist** | Tạo, xóa, quản lý danh sách phát |
| 🤖 **AI Gợi ý nhạc** | Gợi ý bài tương tự dựa trên âm sắc (MFCC + KNN) |
| 🎼 **Phân loại thể loại** | Tự động phân loại genre bằng K-Nearest Neighbors |
| 📝 **Lời bài hát AI** | Tự động tạo LRC (lời có timestamp) bằng Whisper |
| ✏️ **Chỉnh sửa lời** | Giao diện chỉnh sửa lời nhạc thủ công |
| 🎬 **Lyrics Overlay** | Hiển thị lời bài hát theo phong cách Spotify |

---

## 🛠️ Công nghệ sử dụng

- **Backend:** `FastAPI` + `Uvicorn`
- **Database:** `SQLite` (mặc định) hoặc `MySQL`
- **ORM & Migration:** `SQLAlchemy` + `Alembic`
- **AI / Audio:** `librosa`, `scikit-learn`, `numpy`, `openai-whisper`
- **Audio Metadata:** `mutagen`
- **Frontend:** HTML / CSS / Vanilla JavaScript (không cần build)

---

## 💻 Yêu cầu hệ thống

Trước khi bắt đầu, hãy đảm bảo máy bạn đã cài đặt:

- **Python** `3.10` trở lên — [Tải tại đây](https://www.python.org/downloads/)
- **ffmpeg** — Bắt buộc cho Whisper hoạt động

  > **Windows:** Tải ffmpeg tại [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html),
  > giải nén và thêm thư mục `bin/` vào **System PATH**.
  >
  > **macOS:** `brew install ffmpeg`
  >
  > **Linux (Ubuntu/Debian):** `sudo apt install ffmpeg`

- **Git** — [Tải tại đây](https://git-scm.com/)

---

## 🚀 Hướng dẫn cài đặt

Thực hiện **từng bước theo thứ tự** dưới đây.

### Bước 1 — Clone dự án

```bash
git clone https://github.com/tuankhanh2306/Music_player.git
cd Music_player
```

### Bước 2 — Tạo môi trường ảo (Virtual Environment)

> **Khuyến nghị:** Luôn dùng virtualenv để tránh xung đột thư viện với các dự án khác.

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (macOS / Linux)
source venv/bin/activate
```

### Bước 3 — Cài đặt thư viện

```bash
pip install -r requirements.txt
```

> ⚠️ **Lưu ý:** `openai-whisper` và `librosa` khá nặng (~1-2 GB). Quá trình cài đặt có thể mất vài phút.

### Bước 4 — Cấu hình file `.env`

Copy file mẫu và chỉnh sửa theo máy của bạn:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Mở file `.env` và cấu hình:

```env
# --- SQLite (Đơn giản, dùng cho local) ---
DATABASE_URL=sqlite:///./music_db.db

# --- MySQL (Nếu muốn dùng MySQL) ---
# DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/music_db

# Thư mục lưu file nhạc upload
UPLOAD_DIR=uploads

# Thư mục lưu cache AI vectors
FEATURE_CACHE_PATH=data/features.npy

# Giới hạn file upload (MB)
MAX_UPLOAD_SIZE_MB=50

# Định dạng file âm thanh được chấp nhận
ALLOWED_AUDIO_EXTENSIONS=[".mp3",".wav",".flac"]
```

### Bước 5 — Khởi tạo Database

```bash
alembic upgrade head
```

> Lệnh này tạo toàn bộ bảng trong database. Chỉ cần chạy **một lần** khi cài đặt lần đầu.

### Bước 6 — Chạy Server

```bash
uvicorn main:app --reload
```

Sau khi khởi động thành công, truy cập:

| Địa chỉ | Mô tả |
|---|---|
| `http://localhost:8000/app/index.html` | 🎵 Giao diện người dùng |
| `http://localhost:8000/docs` | 📄 Swagger API Documentation |
| `http://localhost:8000/redoc` | 📋 ReDoc API Documentation |

---

## 📁 Cấu trúc dự án

```
Music_player/
├── src/
│   ├── api/                    # FastAPI Routers (song, playlist, recommend)
│   ├── audio_processing/       # Trích xuất MFCC, Whisper LRC
│   ├── database/               # SQLAlchemy engine, CRUD operations
│   ├── models/                 # Định nghĩa bảng (Song, Playlist)
│   ├── recommendation/         # AI Engine (KNN, Cosine Similarity)
│   ├── schemas/                # Pydantic schemas (request/response)
│   ├── core/                   # Logger, Exception handlers
│   ├── config.py               # Đọc biến môi trường (.env)
│   └── frontend/               # Giao diện HTML/CSS/JS
├── alembic/                    # Database migration scripts
├── tests/                      # Unit tests
├── uploads/                    # File nhạc upload (không được commit)
├── data/                       # AI feature cache (.npy, không commit)
├── main.py                     # Entry point khởi chạy server
├── requirements.txt            # Danh sách thư viện Python
├── .env.example                # File cấu hình mẫu
└── alembic.ini                 # Cấu hình Alembic
```

---

## ⚠️ Các lưu ý quan trọng

### 🚫 Dữ liệu bài hát không có sẵn sau khi clone

Do bản quyền, **file nhạc và database không được lưu trong repository**. Sau khi clone về, bạn sẽ có một hệ thống trống. Bạn cần **tự upload nhạc** của mình vào ứng dụng thông qua giao diện web.

### 📂 Thư mục `uploads/` và `data/` sẽ được tạo tự động

Khi chạy server lần đầu, hai thư mục này sẽ được tạo tự động. Đây là nơi lưu trữ file nhạc và file cache AI của bạn — **không nên commit chúng lên Git**.

### 🧠 Lần đầu phát nhạc có thể chậm

Khi upload bài hát lần đầu, Whisper sẽ tự động chạy nền để tạo lời bài hát. Đây là quá trình nặng, có thể mất **vài phút đến hàng chục phút** tùy vào cấu hình máy.

### 📦 `openai-whisper` cần download model

Lần đầu chạy Whisper, nó sẽ tự tải model AI về máy (~150MB). Cần kết nối Internet cho bước này.

### 🔑 File `.env` không được commit

File `.env` chứa thông tin nhạy cảm (mật khẩu database, API keys). File này nằm trong `.gitignore` — **không được commit lên repository**.

---

## 🔧 Troubleshooting

### ❌ Lỗi: `ModuleNotFoundError: No module named 'xxx'`

```bash
# Đảm bảo môi trường ảo đã được kích hoạt
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux

# Cài lại toàn bộ thư viện
pip install -r requirements.txt
```

### ❌ Lỗi: `FileNotFoundError: ffmpeg not found`

ffmpeg chưa được cài hoặc chưa được thêm vào PATH. Xem lại [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống).

```bash
# Kiểm tra ffmpeg đã cài chưa
ffmpeg -version
```

### ❌ Lỗi: Không phát được nhạc / "File nhạc không tồn tại trên server"

Nguyên nhân phổ biến nhất là bạn đang dùng file `music_db.db` cũ (từ máy khác). Hãy xóa nó và khởi tạo lại:

```bash
# Xóa database cũ
del music_db.db       # Windows
rm music_db.db        # macOS/Linux

# Khởi tạo lại
alembic upgrade head
```

Sau đó upload lại nhạc của bạn.

### ❌ Lỗi kết nối MySQL: `Access denied`

Kiểm tra lại thông tin kết nối trong file `.env`:

```env
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```

Đảm bảo database đã được tạo trước:

```sql
CREATE DATABASE music_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### ❌ Lỗi `alembic upgrade head` fails

```bash
# Kiểm tra DATABASE_URL trong .env có đúng không
# Đảm bảo file alembic.ini tồn tại và trỏ đúng script_location
alembic current
```

---

## 🧪 Chạy Tests

```bash
pytest tests/ -v
```

---

## 📄 License

Dự án được xây dựng cho mục đích học thuật. Vui lòng không sử dụng cho mục đích thương mại.