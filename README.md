# 🎵 AI Music Player (100% Python Project)

> Một hệ thống nghe nhạc thông minh được xây dựng hoàn toàn bằng ngôn ngữ Python. Dự án tích hợp trí tuệ nhân tạo (AI) để tự động phân tích sóng âm thanh và gợi ý các bài hát có giai điệu, âm sắc tương đồng.

## 🌟 Giới thiệu dự án
Dự án **AI Music Player** giải quyết bài toán khám phá âm nhạc thông qua **Content-Based Filtering** (Lọc dựa trên nội dung). 

Thay vì phụ thuộc vào các thẻ metadata khô khan (thể loại, tên nghệ sĩ), hệ thống sử dụng sức mạnh xử lý dữ liệu của Python để trực tiếp "nghe" file audio. Thông qua việc trích xuất đặc trưng MFCC (Mel-frequency cepstral coefficients) và áp dụng thuật toán Machine Learning, hệ thống có khả năng tìm ra các bài hát có "màu sắc âm thanh" giống nhau nhất một cách tự động.

## 🚀 Tính năng cốt lõi (Features)
- **Hệ thống nghe nhạc:** Upload file mp3/wav, phát nhạc (stream audio qua API).
- **Quản lý Playlist:** Tạo, quản lý và lưu trữ danh sách phát cá nhân.
- **AI Recommendation:** Gợi ý tức thời top K bài hát có giai điệu tương tự bài đang phát.
- **Tối ưu hóa hiệu năng (Precompute):** Đặc trưng âm thanh được trích xuất và cache ngay khi upload, giúp API AI phản hồi cực kỳ nhanh chóng.

## 🛠 Công nghệ sử dụng (Python Ecosystem)
Dự án thuần Python, không sử dụng các framework ngôn ngữ khác (như Java/NodeJS) cho Backend:
- **Ngôn ngữ lõi:** Python 3.10+
- **Backend API:** `FastAPI` (hoặc `Flask`) & ASGI Server `Uvicorn`
- **AI & Audio Processing:** `librosa` (xử lý âm thanh), `scikit-learn` (thuật toán KNN & Cosine Similarity), `numpy` (xử lý ma trận)
- **Database:** SQLite / MySQL (tương tác qua ORM `SQLAlchemy`)
- **Giao diện (Frontend):** - Tùy chọn 1 (Thuần Python): `Tkinter` hoặc `PyQt`
  - Tùy chọn 2 (Web nhẹ): HTML/CSS/Vanilla JS gọi qua REST API.

---

## 📁 Cấu trúc mã nguồn (Architecture)

```text
ai_music_player/
 ├── .ai/                      # Quy chuẩn dự án và Kế hoạch phát triển
 ├── docs/                     # Tài liệu thiết kế API và Database Schema
 ├── src/                      # Source code chính của hệ thống
 │   ├── api/                  # Routes & Controllers (RESTful API)
 │   ├── audio_processing/     # Logic trích xuất đặc trưng âm thanh (Librosa)
 │   ├── recommendation/       # Logic AI (KNN & Cosine Similarity)
 │   ├── database/             # Kết nối DB & CRUD operations
 │   └── models/               # Định nghĩa các bảng thực thể (SQLAlchemy)
 ├── tests/                    # Unit tests kiểm thử module
 ├── uploads/                  # Thư mục lưu trữ file audio gốc (.mp3, .wav)
 ├── data/                     # Thư mục lưu cache AI vectors (.npy)
 ├── main.py                   # File Entry-point khởi chạy Server
 └── requirements.txt          # Danh sách thư viện Python