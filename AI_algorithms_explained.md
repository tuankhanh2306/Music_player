# 🎵 Giải Thích Toàn Bộ Thuật Toán AI Trong Dự Án Music Player

---

## 📋 TỔNG QUAN — HỆ THỐNG CÓ 3 THUẬT TOÁN AI CHÍNH

| # | Thuật toán | Chức năng | File |
|---|-----------|-----------|------|
| 1 | **MFCC Feature Extraction** | Biến bài hát → vector số | `feature_extraction.py` |
| 2 | **KNN Similarity** (NearestNeighbors) | Gợi ý bài hát tương tự / AI Radio | `knn_model.py`, `engine.py` |
| 3 | **KNN Classifier** (KNeighborsClassifier) | Phân loại thể loại (genre) tự động | `knn_model.py`, `engine.py` |
| ✨ Bonus | **OpenAI Whisper** | Nhận diện giọng nói → lời bài hát LRC | `whisper_service.py` |

---

## 🔷 THUẬT TOÁN 1 — MFCC FEATURE EXTRACTION

### Dạng y = f(x) + b

```
y = [mfcc₁, mfcc₂, ..., mfcc₂₀, tempo, centroid, zcr]
  = f(audio_signal) + 0

x = file audio (sóng âm thô, hàng triệu điểm số)
f = librosa feature extraction pipeline
b = 0 (không có bias, đây là biến đổi thuần túy)
y = vector đặc trưng 23 chiều
```

### Giải thích chi tiết

**Input (x):** File âm thanh (`.mp3`, `.wav`) được load thành mảng số thực `y` (waveform) với sample rate `sr = 22050 Hz`.

**Hàm f(x) — trích xuất 4 loại đặc trưng:**

| Đặc trưng | Số chiều | Ý nghĩa vật lý | Tính thế nào |
|-----------|----------|----------------|-------------|
| **MFCC** | 20 | Âm sắc/kết cấu âm thanh (timbre) | FFT → Mel filterbank → DCT → lấy mean |
| **Tempo (BPM)** | 1 | Nhịp độ bài (chậm/nhanh) | Beat tracking |
| **Spectral Centroid** | 1 | Độ "sáng" của âm (treble/bass) | Trọng tâm tần số → lấy mean |
| **ZCR** | 1 | Độ "gắt/nhiễu" (snare, hi-hat) | Số lần tín hiệu cắt qua 0 |

**Output (y):** Vector **23 chiều** cho mỗi bài hát.

```python
combined_vector = np.hstack((mfcc_vector, [tempo_val, centroid_val, zcr_val]))
# Shape: (23,)
```

### 🧠 Sự thông minh ở đâu?

> **MFCC mô phỏng cách tai người nghe âm thanh.** Thay vì so sánh từng mẫu sóng âm (không hiệu quả), hệ thống trích xuất các đặc trưng cấp cao mà con người dùng để phân biệt âm nhạc: nhịp điệu, độ trong trẻo, âm sắc.

- Hai bài nhạc EDM → Tempo cao (~140 BPM), Centroid cao (âm chói)
- Hai bài Ballad → Tempo thấp (~70 BPM), MFCC mềm mại

### 📊 Dataset & Siêu tham số

| Thuộc tính | Giá trị |
|-----------|---------|
| **Dataset nguồn** | Thư viện nhạc của người dùng upload lên hệ thống |
| **Đối tượng** | Mỗi bài hát = 1 đối tượng |
| **Nhãn** | Không có nhãn (unsupervised feature extraction) |
| **Siêu tham số** | `n_mfcc = 20`, `sr = 22050 Hz` |

---

## 🔷 THUẬT TOÁN 2 — KNN SIMILARITY (Gợi ý bài tương tự / AI Radio)

### Dạng y = f(x) + b

```
y = [song_id_1, song_id_2, ..., song_id_k]   ← top-k bài tương tự
  = f(x_query, X_train)

x_query = vector 23 chiều của bài đang nghe (đã chuẩn hoá)
X_train = ma trận [N × 23] của N bài trong thư viện (đã chuẩn hoá)
f       = NearestNeighbors.kneighbors() — tìm k hàng xóm gần nhất
b       = 0
```

### Quy trình từng bước

#### Bước 1: Chuẩn hoá (StandardScaler)
```
x_scaled = (x - μ) / σ

Tại sao cần? → Tempo ~120, MFCC ~-200 đến +100, ZCR ~0.1
   → Không scale thì Tempo "lấn át" toàn bộ, KNN bị lệch
```

#### Bước 2: Tính khoảng cách Cosine
```
distance(A, B) = 1 - (A · B) / (||A|| × ||B||)

Cosine = 0   → hai bài giống hệt nhau
Cosine = 1   → hai bài hoàn toàn khác nhau
```

> **Tại sao dùng Cosine thay Euclidean?**
> Cosine đo **góc** giữa hai vector (hướng âm nhạc), không đo **khoảng cách tuyệt đối** → robust hơn với bài ngắn/dài.

#### Bước 3: Lấy top-k hàng xóm
```python
distances, indices = model.kneighbors(target_vector, n_neighbors=top_k+1)
# Loại bỏ chính bài đang query → trả về top_k bài còn lại
```

### 🧠 Sự thông minh ở đâu?

> Hệ thống **không cần biết tên thể loại** để tìm bài tương tự. Chỉ cần vector âm thanh → tự tìm bài "nghe gần giống" về mặt âm học. Đây là **Unsupervised Similarity Search**.

### 📊 Dataset & Siêu tham số

| Thuộc tính | Giá trị |
|-----------|---------|
| **Dataset** | `data/features.npy` — dict `{song_id: vector_23_chiều}` |
| **Đối tượng** | Các bài hát trong thư viện (N bài) |
| **Nhãn** | ❌ Không có nhãn |
| **`n_neighbors` (K)** | `min(7, N)` — tối đa 7, tùy số bài trong thư viện |
| **`metric`** | `cosine` |
| **`algorithm`** | `brute` (tính toán toàn bộ, phù hợp dataset nhỏ) |
| **Model lưu tại** | `data/knn_model.pkl` |

### AI Radio — Chuỗi Chaining

```
AI Radio = KNN lặp nhiều vòng:

Bài A → KNN → [B, C, D, ...]
         Chọn B (chưa visited)
Bài B → KNN → [A, E, F, ...]
         Chọn E (A đã visited)
Bài E → KNN → [G, H, ...]
         Chọn G...

Kết quả queue: [A, B, E, G, ...]
```

---

## 🔷 THUẬT TOÁN 3 — KNN CLASSIFIER (Phân Loại Thể Loại)

### Dạng y = f(x) + b

```
y = "Pop" / "EDM" / "Ballad" / ...   ← nhãn thể loại được dự đoán
  = argmax(majority_vote_weighted(K_neighbors))

x = vector 23 chiều của bài mới (chưa có nhãn)
f = KNeighborsClassifier.predict()
b = 0
```

### Quy trình từng bước

#### Bước 1: Pipeline chuẩn hoá
```python
clf = make_pipeline(
    StandardScaler(),        # Chuẩn hoá về μ=0, σ=1
    KNeighborsClassifier(
        n_neighbors=7,
        weights="distance",  # Trọng số theo khoảng cách
        metric="cosine"
    )
)
```

#### Bước 2: Majority Voting có trọng số
```
Tìm K=7 hàng xóm gần nhất → xem nhãn genre của từng hàng xóm:

Hàng xóm 1 (d=0.05) → "EDM"      w = 1/0.05 = 20
Hàng xóm 2 (d=0.08) → "EDM"      w = 1/0.08 = 12.5
Hàng xóm 3 (d=0.12) → "Pop"      w = 1/0.12 = 8.3
Hàng xóm 4 (d=0.15) → "EDM"      w = 1/0.15 = 6.7
Hàng xóm 5 (d=0.20) → "Ballad"   w = 1/0.20 = 5.0
...

Tổng vote EDM = 20 + 12.5 + 6.7 = 39.2  ← WINNER
Tổng vote Pop = 8.3
→ y_pred = "EDM"  (confidence = 39.2 / sum_all × 100%)
```

#### Bước 3: Trả về confidence
```python
proba = clf.predict_proba(vector)
confidence = float(np.max(proba)) * 100  # ví dụ: 78.5%
```

### 🧠 Sự thông minh ở đâu?

> **Học từ ví dụ có nhãn của người dùng.** Khi bạn đánh nhãn "Pop" cho một bài, hệ thống học rằng bài hát với vector âm thanh đó thuộc "Pop". Với bài mới, nó tìm các bài đã biết nhãn tương tự → bỏ phiếu → đưa ra gợi ý.

> **`weights="distance"`** là điểm thông minh: bài gần hơn **ảnh hưởng nhiều hơn** đến kết quả, thay vì mỗi bài có 1 phiếu bằng nhau.

### 📊 Dataset & Siêu tham số

| Thuộc tính | Giá trị |
|-----------|---------|
| **Dataset** | Bài hát trong DB có trường `genre` được điền sẵn |
| **Đối tượng** | Bài hát có nhãn genre |
| **Số nhãn (classes)** | Phụ thuộc vào thư viện nhạc của người dùng (tối thiểu 2) |
| **`n_neighbors` (K)** | `min(7, N_labeled)` |
| **`weights`** | `"distance"` — trọng số theo khoảng cách |
| **`metric`** | `"cosine"` |
| **Model lưu tại** | `data/genre_classifier.pkl` |

> **Điều kiện hoạt động:** Cần ít nhất **2 thể loại khác nhau** và ít nhất **2 bài có nhãn genre**.

---

## 🔷 THUẬT TOÁN 4 — OPENAI WHISPER (Speech-to-Text → LRC)

### Dạng y = f(x) + b

```
y = "[00:12.34] Lời câu đầu tiên\n[00:15.80] Câu tiếp theo..."
  = f(audio_waveform)

x = file audio (.mp3/.wav)
f = Whisper Encoder-Decoder (Transformer)
b = 0
y = chuỗi LRC (lời bài hát có dấu thời gian)
```

### Kiến trúc Whisper (bên trong)

```
Audio → [Log-Mel Spectrogram] → [Encoder CNN+Transformer] → [Decoder Transformer] → Text + Timestamps

                    x                      f(x)                      y
```

Whisper là mô hình **Sequence-to-Sequence** dựa trên Transformer:
- **Encoder:** Phân tích âm thanh, tạo context embedding
- **Decoder:** Sinh ra văn bản từng token, kèm timestamp

### 🧠 Sự thông minh ở đâu?

> Whisper được **pre-trained trên 680.000 giờ âm thanh** từ internet — bao gồm tiếng Anh, Việt, Nhật, Hàn... Nó tự động nhận diện ngôn ngữ và phiên âm mà không cần config.

| Khả năng | Mô tả |
|---------|-------|
| **Multi-language** | Tự detect ngôn ngữ (`language=None`) |
| **Timestamp** | Trả về `start`, `end` của từng segment |
| **Noise robust** | Xử lý được nhạc nền |

### 📊 Dataset & Siêu tham số

| Thuộc tính | Giá trị |
|-----------|---------|
| **Dataset** | Pre-trained sẵn (không cần train lại) |
| **Model size** | `"base"` — ~74M parameters (cân bằng tốc độ/chất lượng) |
| **Siêu tham số** | `word_timestamps=False` (theo segment, không theo từng chữ) |
| **Task** | `"transcribe"` (giữ nguyên ngôn ngữ gốc) |

---

## 🔶 TỔNG HỢP — SO SÁNH CÁC THUẬT TOÁN

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE TỔNG THỂ                            │
│                                                                  │
│  File MP3/WAV                                                    │
│      │                                                           │
│      ├─→ [MFCC Extraction] → vector 23D                         │
│      │        │                                                  │
│      │        ├─→ [KNN Similarity] → Bài hát tương tự           │
│      │        │                   → AI Radio queue              │
│      │        │                                                  │
│      │        └─→ [KNN Classifier] → Genre prediction           │
│      │                              (nếu có bài có nhãn)        │
│      │                                                           │
│      └─→ [Whisper STT] → LRC lyrics (lời + timestamp)           │
└─────────────────────────────────────────────────────────────────┘
```

| | MFCC | KNN Similarity | KNN Classifier | Whisper |
|--|------|---------------|----------------|---------|
| **Loại** | Feature Extraction | Unsupervised | Supervised | Deep Learning |
| **Cần nhãn?** | ❌ | ❌ | ✅ (genre) | ❌ (pre-trained) |
| **Input x** | Audio file | Vector 23D | Vector 23D | Audio file |
| **Output y** | Vector 23D | List song IDs | Genre string | LRC string |
| **Dataset** | Bài hát user | features.npy | DB có genre | 680K hours (pre-trained) |
| **Train lại?** | Không (mỗi bài) | Có (sau mỗi upload) | Có (sau mỗi upload) | Không |

---

## 📌 TÓM TẮT SIÊU THAM SỐ QUAN TRỌNG NHẤT

| Siêu tham số | Thuật toán | Giá trị hiện tại | Ảnh hưởng |
|-------------|-----------|-----------------|----------|
| `n_mfcc` | MFCC | **20** | Số chiều MFCC. Tăng → chi tiết hơn nhưng chậm hơn |
| `sr` | MFCC | **22050 Hz** | Sample rate. Chuẩn của librosa |
| `K` (n_neighbors) | KNN Similarity | **min(7, N)** | Tăng K → gợi ý đa dạng hơn, giảm K → chính xác hơn |
| `K` (n_neighbors) | KNN Classifier | **min(7, N)** | Tăng K → mượt hơn, giảm K → nhạy cảm hơn |
| `weights` | KNN Classifier | **"distance"** | Bài gần hơn = phiếu bầu nặng hơn |
| `metric` | Cả 2 KNN | **"cosine"** | Đo góc, phù hợp với vector âm thanh |
| `model_size` | Whisper | **"base"** | Nhỏ hơn ("tiny") = nhanh hơn; Lớn hơn ("medium") = chính xác hơn |
