Tôi đang xây dựng một hệ thống AI Music Player. Hãy hiểu rõ toàn bộ kiến trúc, yêu cầu và viết code cho cả Python AI service và Java Spring Boot backend.

```text
e:\\MP3\\
│
├── ai-service/                        # 🐍 THƯ MỤC CHỨA PYTHON AI SERVICE
│   ├── requirements.txt               # Các thư viện Python cần cài (librosa, flask, sklearn...)
│   ├── app.py                         # Điểm bắt đầu của Flask API (Khởi tạo server)
│   ├── audio_processing.py            # Logic đọc audio và trích xuất MFCC librosa
│   ├── similarity.py                  # Logic tính Cosine Similarity
│   ├── recommendation.py              # Logic tìm top K bài hát (KNN)
│   ├── precompute.py                  # Script chạy tay để duyệt file và tính map features
│   ├── test_recommendation.py         # Chứa đoạn code test đơn giản
│   └── data/
│       └── features.npy               # Nơi lưu trữ vector precompute (sinh ra tự động)
│
├── java-backend/                      # ☕ THƯ MỤC CHỨA JAVA SPRING BOOT
│   ├── pom.xml / build.gradle         # File quản lý thư viện Maven/Gradle
│   ├── uploads/                       # 📂 Nơi lưu trữ vật lý các file MP3/WAV do user tải lên
│   └── src/
│       └── main/
│           ├── resources/
│           │   └── application.yml    # File cấu hình kết nối Database, cổng (port 8080)
│           └── java/
│               └── com/musicplayer/
│                   ├── MusicPlayerApplication.java  # File khởi chạy Spring Boot
│                   ├── config/
│                   │   └── RestTemplateConfig.java  # Cấu hình WebClient để gọi sang Python AI
│                   ├── controller/
│                   │   ├── SongController.java      # API: Upload file nhac, Stream MP3, Get All
│                   │   └── RecommendController.java # API: Chuyển tiếp recommend tới Python
│                   ├── service/
│                   │   ├── StorageService.java      # Logic lưu/đọc file từ thư mục uploads/
│                   │   ├── SongService.java         # Logic tương tác Database bài hát
│                   │   └── AiServiceClient.java     # Hàm Call tới Python Flask API
│                   ├── repository/
│                   │   ├── SongRepository.java      # Spring Data JPA cho Song
│                   │   ├── PlaylistRepository.java  ...
│                   │   └── UserRepository.java      ...
│                   └── entity/
│                       ├── Song.java                # Schema Database (id, title, filepath...)
│                       ├── Playlist.java            ...
│                       └── User.java                ...
│
├── PLAN.md                            # File kế hoạch làm việc
└── README.md                          # File yêu cầu bài toán
```

=====================
1. MỤC TIÊU HỆ THỐNG
=====================
- Xây dựng ứng dụng nghe nhạc có AI recommendation
- Người dùng có thể:
  + Phát nhạc
  + Tìm kiếm bài hát
  + Tạo playlist
  + Nhận gợi ý bài hát tương tự

=====================
2. KIẾN TRÚC HỆ THỐNG
=====================
Hệ thống gồm 3 phần:

(1) Frontend:
- Gửi request HTTP
- Phát nhạc

(2) Java Backend (Spring Boot):
- REST API
- Quản lý user, playlist, song metadata
- Streaming audio
- Gọi Python AI service

(3) Python AI Service:
- Xử lý audio
- Recommendation system

=====================
3. LƯU TRỮ DỮ LIỆU
=====================
- Audio file: lưu trong thư mục /uploads
- Metadata: MySQL/PostgreSQL
- Feature AI: lưu file (.npy) hoặc memory

=====================
4. LUỒNG HOẠT ĐỘNG
=====================
- User phát nhạc → frontend gọi Java
- Java stream file mp3 về client
- Java lưu history
- Khi cần recommend:
  Java gọi Python → Python trả về danh sách bài

=====================
5. PYTHON AI SERVICE (BẮT BUỘC CODE)
=====================

Yêu cầu:
- Dùng Python + librosa + numpy + scikit-learn

Chức năng:
1. Trích xuất feature:
   - Sử dụng MFCC
2. Tính similarity:
   - Cosine Similarity
3. Recommendation:
   - KNN (top K bài giống nhất)
4. Sorting:
   - Sắp xếp theo độ tương đồng
5. Searching:
   - Tìm bài theo id

Yêu cầu:
- Tách module:
  + audio_processing.py
  + similarity.py
  + recommendation.py
- Có API Flask:

POST /recommend
Input:
{
  "song_id": 1
}

Output:
{
  "recommended": [2, 5, 8]
}

- Precompute feature (không tính lại mỗi request)

=====================
6. JAVA BACKEND (BẮT BUỘC CODE)
=====================

Sử dụng Spring Boot

Yêu cầu:

1. Entity:
- Song (id, title, artist, file_path)
- User
- Playlist

2. API:

- Upload bài hát
POST /songs/upload

- Lấy danh sách bài hát
GET /songs

- Stream audio
GET /songs/{id}

- Recommendation
GET /recommend/{songId}

3. Logic:
- Lưu file audio vào /uploads
- Lưu metadata vào DB
- Khi gọi /recommend:
  → Java gọi Python API:
     http://localhost:5000/recommend
  → Nhận kết quả → trả về client

4. Code structure:
- Controller
- Service
- Repository (JPA)
- Entity

=====================
7. YÊU CẦU TỐI ƯU
=====================
- Precompute MFCC
- Dùng KNN để giảm số phép tính
- Sorting top K
- Không xử lý audio realtime
- Code rõ ràng, dễ hiểu

=====================
8. OUTPUT YÊU CẦU
=====================
- Viết đầy đủ code:
  + Python AI service
  + Java Spring Boot backend
- Code phải chạy được
- Có ví dụ test
- Giải thích ngắn gọn từng phần