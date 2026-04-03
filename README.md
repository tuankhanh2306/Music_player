# 🎵 AI Music Player System

![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-F2F4F9?style=for-the-badge&logo=spring-boot)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)

Hệ thống phát nhạc trực tuyến tích hợp trí tuệ nhân tạo (AI) để gợi ý bài hát dựa trên nội dung âm thanh (Content-based Recommendation). 

Dự án được xây dựng theo kiến trúc Microservices cơ bản, tách biệt giữa core xử lý nghiệp vụ/streaming (Java Spring Boot) và service phân tích âm thanh bằng học máy (Python).

## 📑 Mục lục
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Tính năng chính](#-tính-năng-chính)
- [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
- [Luồng thuật toán AI](#-luồng-thuật-toán-ai)
- [Cài đặt & Khởi chạy](#-cài-đặt--khởi-chạy)
- [Tài liệu API](#-tài-liệu-api)

---

## 🏗 Kiến trúc hệ thống

Hệ thống bao gồm 3 thành phần chính:
1. **Frontend:** Xử lý giao diện người dùng, gửi HTTP request và phát nhạc thông qua luồng stream.
2. **Backend (Java Spring Boot):** Quản lý metadata bài hát (MySQL/PostgreSQL), người dùng, playlist, xử lý upload file vật lý và streaming audio dạng byte-range. Chịu trách nhiệm giao tiếp với AI Service.
3. **AI Service (Python Flask):** Đảm nhiệm việc trích xuất đặc trưng âm thanh và thực thi thuật toán gợi ý.

---

## ✨ Tính năng chính

- **Quản lý âm nhạc:** Upload file MP3/WAV, lưu trữ vật lý và quản lý metadata.
- **Streaming Audio:** Hỗ trợ phát nhạc mượt mà thông qua kỹ thuật truyền luồng.
- **AI Recommendation:** - Gợi ý top K bài hát tương tự nhau hoàn toàn tự động khi người dùng đang nghe nhạc.
  - Tối ưu hóa hiệu năng thông qua cơ chế Precompute đặc trưng (Feature Map) và K-Nearest Neighbors (KNN).

---

## 📂 Cấu trúc thư mục

```text
📦 ai-music-player
 ┣ 📂 ai-service/                # 🐍 Python AI Service
 ┃ ┣ 📜 app.py                   # Điểm bắt đầu của Flask API 
 ┃ ┣ 📜 audio_processing.py      # Trích xuất MFCC với librosa
 ┃ ┣ 📜 similarity.py            # Tính Cosine Similarity
 ┃ ┣ 📜 recommendation.py        # Logic tìm top K bài hát (KNN)
 ┃ ┣ 📜 precompute.py            # Script chạy batch tính map features
 ┃ ┣ 📜 test_recommendation.py   # Script test AI độc lập
 ┃ ┣ 📂 data/                    # Nơi lưu trữ vector precompute (.npy)
 ┃ ┗ 📜 requirements.txt         
 ┃
 ┣ 📂 java-backend/              # ☕ Java Spring Boot Backend
 ┃ ┣ 📂 uploads/                 # Nơi lưu trữ vật lý audio files
 ┃ ┣ 📂 src/main/java/com/musicplayer/
 ┃ ┃ ┣ 📂 config/                # Cấu hình WebClient/RestTemplate
 ┃ ┃ ┣ 📂 controller/            # Định nghĩa các REST API
 ┃ ┃ ┣ 📂 service/               # Logic nghiệp vụ & AI Client
 ┃ ┃ ┣ 📂 repository/            # Spring Data JPA
 ┃ ┃ ┗ 📂 entity/                # Database Schema (Song, User, Playlist)
 ┃ ┣ 📜 pom.xml                  
 ┃ ┗ 📜 application.yml          # Cấu hình DB, Port