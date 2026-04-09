# Kế Hoạch Triển Khai: AI Music Player (Team 5 Members)

## 1. Giai đoạn 0: "The Contract" (Cả Team cùng chốt - BẮT BUỘC)
Để 5 người làm song song không bị xung đột, toàn team phải hoàn thành Phase này trước tiên.
- [ ] Thiết lập thư mục gốc và đẩy lên GitHub (Main repo).
- [ ] Chốt Database Schema (Các trường trong bảng Song, User, Playlist, History).
- [ ] Chốt API Specs (Định nghĩa rõ request/response JSON cho từng API, lưu vào `docs/api_specs.md`).
- [ ] Chốt AI I/O (Đầu vào của hàm AI là gì, đầu ra là mảng `[song_id1, song_id2,...]`).

---

## 2. Các Luồng Phát Triển Độc Lập (Parallel Tracks)

### Track 1: Database & Models (Thành viên 1 - Data Engineer)
*Nhiệm vụ: Xây dựng nền tảng lưu trữ. Không cần quan tâm AI hay API hoạt động ra sao.*
- [ ] Viết các file trong `models/` (song.py, user.py, playlist.py, history.py) bằng SQLAlchemy/Pydantic.
- [ ] Viết file `database/db.py` để setup kết nối SQLite/MySQL.
- [ ] Viết file `database/crud.py` chứa các hàm (Insert bài hát, Get by ID, Add to playlist...).
- [ ] Tạo script tự động seed data (thêm 10-20 bài hát giả vào DB để các bạn khác test).

### Track 2: Core API & Routing (Thành viên 2 - Backend Engineer)
*Nhiệm vụ: Xây dựng các cổng giao tiếp API. Tạm thời dùng Mock Data trả về nếu DB hoặc AI chưa xong.*
- [ ] Setup `main.py` và chạy server FastAPI/Flask.
- [ ] Viết `api/song_routes.py`: Xử lý logic Upload file (lưu vào `/uploads`) và stream file audio trả về Frontend.
- [ ] Viết `api/playlist_routes.py`: Logic thêm/sửa/xóa playlist.
- [ ] Viết `api/recommend_routes.py`: Nhận request gợi ý (Tạm thời hardcode trả về mảng `[1, 2, 3]` trước khi ghép AI).

### Track 3: Audio Processing (Thành viên 3 - Data Scientist)
*Nhiệm vụ: Chỉ làm việc với file âm thanh vật lý `.mp3/.wav`. Không cần gọi DB hay API.*
- [ ] Viết file `audio_processing/feature_extraction.py`.
- [ ] Viết hàm đọc file audio bằng `librosa`.
- [ ] Viết logic trích xuất đặc trưng MFCC từ audio.
- [ ] Viết hàm chuyển MFCC thành 1 vector 1 chiều và lưu ra file `data/features.npy`.
- [ ] (Testing): Tự tải 5 bài hát mp3 về test thử xem hàm có chạy ra đúng mảng numpy không.

### Track 4: AI Recommendation Engine (Thành viên 4 - ML Engineer)
*Nhiệm vụ: Viết thuật toán gợi ý. Nhận vào file `.npy` và ID, trả ra ID các bài giống nhất.*
- [ ] Viết file `recommendation/similarity.py`: Tính Cosine Similarity giữa các vector.
- [ ] Viết file `recommendation/knn_model.py`: Cấu hình thuật toán K-Nearest Neighbors bằng `scikit-learn`.
- [ ] Viết `recommendation/engine.py`: Kết hợp KNN và Cosine để nhận vào `song_id` -> load mảng đặc trưng -> trả ra top 5 `song_id` tương đồng.
- [ ] (Testing): Tự tạo một mảng Numpy giả (Mock Data) gồm các con số ngẫu nhiên để test thuật toán KNN, không cần đợi Thành viên 3 làm xong âm thanh.

### Track 5: Frontend & Integration (Thành viên 5 - Frontend Engineer)
*Nhiệm vụ: Làm giao diện Web hoặc Desktop. Dùng Postman Mock Server hoặc test với local nếu API chưa xong.*
- [ ] Thiết kế giao diện HTML/JS (hoặc Tkinter/PyQt).
- [ ] Viết chức năng Call API upload bài hát (`POST /songs/upload`).
- [ ] Viết chức năng Music Player (Nhận luồng stream từ `GET /songs/{id}` và phát nhạc).
- [ ] Viết phần UI hiển thị "Danh sách gợi ý" (Gọi `GET /recommend/{songId}`).

---

## 3. Giai đoạn 3: Hội quân & Tích hợp (Integration Phase)
Khi 5 Track đã xong, tiến hành ghép nối các mảnh ghép.
- [ ] Ghép API (Track 2) kết nối với DB thực (Track 1) thay vì Mock data.
- [ ] Gắn hàm Extract MFCC (Track 3) vào API Upload (Track 2) -> Để mỗi khi up nhạc tự động tính toán AI.
- [ ] Gắn Model Gợi ý (Track 4) vào API Recommendation (Track 2).
- [ ] Frontend (Track 5) gọi API thực tế và fix các lỗi CORS (nếu có).
- [ ] Kiểm thử toàn bộ hệ thống (End-to-End Test).