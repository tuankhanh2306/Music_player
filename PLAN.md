# 📋 Kế Hoạch Triển Khai Hệ Thống AI Music Player

Hệ thống bao gồm 3 phần chính: Frontend, Java Spring Boot Backend, và Python AI Service. Dưới đây là kế hoạch chi tiết để triển khai phần Backend và AI Service.

---

## 🛠️ 1. Khởi tạo Project & Môi trường

### 1.1 Python AI Service
- [ ] Tạo thư mục `ai-service`
- [ ] Tạo môi trường ảo (virtual environment)
- [ ] Tạo file `requirements.txt` và cài đặt các thư viện:
  - `librosa` (Xử lý audio)
  - `numpy`, `scipy` / `scikit-learn` (Toán học, KNN, Cosine Similarity)
  - `flask` (REST API)

### 1.2 Java Spring Boot Backend
- [ ] Khởi tạo project Spring Boot (ví dụ qua Spring Initializr)
- [ ] Bổ sung các dependencies:
  - `Spring Web` (REST API)
  - `Spring Data JPA` (Tương tác Database)
  - `MySQL Driver` hoặc `PostgreSQL Driver` (Database)
  - `Lombok` (Giảm boilerplate code)
- [ ] Tạo thư mục `uploads` để lưu trữ file audio chuẩn bị stream

---

## 🐍 2. Xây dựng Python AI Service

### 2.1 Xử lý Audio & Đặc trưng (`audio_processing.py`)
- [ ] Viết hàm đọc file audio (hỗ trợ MP3/WAV)
- [ ] Sử dụng `librosa` để trích xuất đặc trưng MFCC
- [ ] Xử lý vector (vd: tính `mean` qua trục thời gian hoặc `flatten`) để có feature vector 1 chiều đại diện cho bài hát

### 2.2 Tính độ tương đồng & Gợi ý (`similarity.py` & `recommendation.py`)
- [ ] Cài đặt thuật toán độ đo **Cosine Similarity**
- [ ] Áp dụng **K-Nearest Neighbors (KNN)** để tìm tập hợp bài hát gần nhất dựa trên Cosine distance
- [ ] Implement luồng **Sorting**: sắp xếp các bài tương tự theo độ tương đồng giảm dần
- [ ] Implement luồng **Searching**: tìm bài hát bằng `song_id` để lấy feature mẫu so sánh

### 2.3 Cơ chế Precompute & Lưu trữ
- [ ] Viết script dạng job/worker duyệt qua thư mục audio để trích xuất feature sẵn
- [ ] Trích xuất feature của toàn bộ kho nhạc và lưu thành file `features.npy` hoặc pickle dictionary
- [ ] Viết hàm nạp file `features.npy` vào bộ nhớ lúc khởi động app (tránh tính lại khi request)

### 2.4 Xây dựng REST API (`app.py`)
- [ ] Khởi tạo Flask Application
- [ ] Định nghĩa API `POST /recommend`:
  - **Input**: `{ "song_id": 1 }`
  - **Logic**: Tìm feature của `song_id` $\rightarrow$ gọi hàm KNN $\rightarrow$ lọc top K
  - **Output**: `{ "recommended": [2, 5, 8] }`

---

## ☕ 3. Xây dựng Java Spring Boot Backend

### 3.1 Cấu hình Database & Storage
- [ ] Cấu hình file `application.yml`/`application.properties` để kết nối tới MySQL/PostgreSQL
- [ ] Cấu hình tham số thư mục lưu file (ví dụ: `app.upload.dir=/uploads`)

### 3.2 Entities & JPA Repositories
- [ ] Tạo entity `User` (id, username, password...)
- [ ] Tạo entity `Song` (id, title, artist, file_path, upload_time...)
- [ ] Tạo entity `Playlist` (id, name, user_id, danh sách bài hát...)
- [ ] Tạo các interface `SongRepository`, `UserRepository`, `PlaylistRepository` kế thừa `JpaRepository`

### 3.3 Tầng Service Layer
- [ ] `StorageService`: Chịu trách nhiệm Lưu file tải lên vào thư mục `/uploads` và Đọc file để streaming
- [ ] `SongService`: Quản lý logic thêm mới bài hát, lưu metadata vào DB
- [ ] `RecommendationService`:
  - Gọi HTTP Client (e.g., `RestTemplate` / `WebClient`)
  - Gửi request tới Python API `http://localhost:5000/recommend` kèm `songId`
  - Nhận và parse kết quả trả về list `Song` tương ứng

### 3.4 Tầng Controller (REST APIs)
- [ ] `POST /songs/upload`: Nhận file Multipart, lưu audio file vật lý và tạo bản ghi vào DB
- [ ] `GET /songs`: Trả về danh sách quản lý các bài hát (có phân trang)
- [ ] `GET /songs/{id}`: Đầu cuối (endpoint) để **Streaming Audio** về frontend phát nhạc (trả về byte ranges)
- [ ] `GET /recommend/{songId}`: Gọi sang Python API và trả về danh sách đối tượng bài hát gợi ý cho frontend

---

## 🔗 4. Tích hợp và Kiểm thử (Integration & Testing)

### 4.1 Unit Test / API Test
- [ ] (Python) Viết script test nhỏ nạp 2 file audio và in độ đo tự tính ra màn hình
- [ ] (Python) Test Flask API `/recommend` qua cURL hoặc Postman
- [ ] (Java) Dùng Postman test up file `POST /songs/upload`
- [ ] (Java) Kiểm tra stream trực tiếp `GET /songs/{id}` trên trình duyệt

### 4.2 End-to-End Test (E2E Test)
- [ ] Chạy Python service ở port 5000
- [ ] Chạy Spring Boot backend ở port 8080
- [ ] Gửi yêu cầu qua `GET /recommend/{songId}` trên Spring Boot, kiểm tra xem nó có gọi đúng Python service không và trả về mảng bài hát tương tự chuẩn xác hay không.

---

## ✅ Tổng kết Trạng Thái

| Thành phần | Trạng thái |
|:---|:---:|
| Khởi tạo Python Service | ⏳ Cần làm |
| Python Audio Processing & KNN | ⏳ Cần làm |
| Python Flask API & Precompute | ⏳ Cần làm |
| Khởi tạo Spring Boot | ⏳ Cần làm |
| Java Entities & Database | ⏳ Cần làm |
| Java Storage & Streaming API | ⏳ Cần làm |
| Java REST Integration API | ⏳ Cần làm |
| Test Integration E2E | ⏳ Cần làm |
