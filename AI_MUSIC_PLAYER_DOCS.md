# TÀI LIỆU KỸ THUẬT: AI MUSIC PLAYER
*Dành cho báo cáo chuyên môn, thuyết trình và bảo vệ đồ án.*

---

## PHẦN 1: LUỒNG HOẠT ĐỘNG CỦA HỆ THỐNG (SYSTEM WORKFLOW)

Hệ thống AI Music Player hoạt động dựa trên phương pháp **Content-Based Filtering** (Gợi ý dựa trên nội dung sóng âm), hoàn toàn không phụ thuộc vào dữ liệu lịch sử nghe nhạc của người dùng. Hệ thống gồm 2 luồng (Flow) cốt lõi:

### 1.1. Luồng Tải Nhạc và Nhận Diện Thể Loại (AI Analyzer Flow)
Đây là quy trình khép kín giúp số hóa và phân tích âm thanh theo thời gian thực (Real-time).

*   **Bước 1: Tải file lên (Client-side):** Người dùng kéo thả file `.mp3`/`.wav` vào giao diện.
*   **Bước 2: Phân tích sóng âm ngầm (API `/songs/analyze`):**
    *   File được lưu vào bộ nhớ tạm (`temp`).
    *   Thư viện lõi (Librosa) tiến hành mổ xẻ âm thanh, trích xuất Vector đặc trưng (Audio Fingerprint) gồm 23 chiều.
*   **Bước 3: Dự đoán & Đánh giá mức độ tự tin (Majority Voting):**
    *   Vector 23 chiều được chuẩn hóa (Scale) và đưa vào Mô hình KNN Classifier.
    *   Hệ thống lục tìm $K$ bài hát giống nhất trong cơ sở dữ liệu để "bầu chọn" thể loại (Genre) và tính toán độ tự tin (Confidence Score %).
*   **Bước 4: Trả kết quả & Nhận xác nhận:** UI Backend trả kết quả. Giao diện (Frontend) hiển thị dự đoán (VD: _"EDM (92%)"_). User có quyền thay đổi hoặc Chấp nhận.
*   **Bước 5: Lưu trữ & Tái huấn luyện (Retrain):** System lưu file chính thức vào ổ cứng `/uploads`, lưu Record vào SQLite, cập nhật Vector Array (`.npy`) và kích hoạt Background Task để huấn luyện lại toàn bộ mô hình KNN nhằm bao gồm dữ liệu mới.

### 1.2. Luồng Phát Nhạc Tự Động (AI Radio / Recommendation Flow)
Khắc phục điểm yếu "chỉ shuffle ngẫu nhiên" của trình phát nhạc thông thường.

*   **Bước 1: Khởi nguồn (Seed):** Khi user đang nghe một bài hát và nhấn nút "AI Radio".
*   **Bước 2: Truy vấn Không gian Vector:** Hệ thống trích xuất ID bài hát hiện tại, lấy Vector 23 chiều tương ứng từ biến Cache (RAM).
*   **Bước 3: Tìm kiếm Láng giềng (Similarity Search):** Thuật toán Machine Learning đo lường khoảng cách hình học của Vector Seed với hàng nghìn Vector khác trong csdl. Khoảng cách càng ngắn = càng giống nhau về nhịp điệu và âm sắc.
*   **Bước 4: Phục vụ Playlist:** Hệ thống sắp xếp 20 bài có khoảng cách ngắn nhất, trả về Frontend dưới dạng Playlist liên tục (Queue).

---

## PHẦN 2: THUẬT TOÁN ALGORITHMS VÀ CÔNG THỨC TOÁN HỌC

Hệ thống AI Music Player sử dụng 2 kỹ thuật chính trong xử lý âm thanh kỹ thuật số và Học máy.

### 2.1. Trích Xuất Đặc Trưng (Feature Extraction)
Biến đổi sóng âm thanh thời gian thực (Time-domain) thành dữ liệu số hóa có cấu trúc: Biểu diễn bài hát dưới dạng véc-tơ không gian toán học $X \in \mathbb{R}^{n}$.

Mỗi bài hát $S$ được chuyển hóa thành Vector $\mathbf{x}$:
**$\mathbf{x} = [x_1, x_2, \dots, x_{23}]$**

Các thành phần của $\mathbf{x}$:
1.  **MFCC (20 chiều):** Đặc trưng biểu diễn âm sắc (Timbre) / Thanh quản nghệ sĩ.
2.  **Tempo (1 chiều):** Đặc trưng biểu thị vận tốc nhịp tim bài hát (BPM), giúp model tách biệt nhạc quẩy (EDM > 120 BPM) và Ballad (< 90 BPM).
3.  **Spectral Centroid (1 chiều):** Trọng tâm quang phổ, đo độ "chói/sáng" của nhạc cụ (đặc biệt bắt rất rõ tiếng Synth của Vinahouse/EDM).
4.  **Zero-Crossing Rate (1 chiều - ZCR):** Xác định cường độ xuất hiện của các tạp âm cụt lủn (tiếng trống Snare, hi-hat của nhạc Rap/Trap).

### 2.2. Chuẩn hóa dữ liệu (Standardization / Z-score)
Vì Tempo dao động quanh trị số 120, trong khi ZCR chỉ ở mức 0.05, ta phải đưa tất cả phương sai n-chiều về cùng một tỷ lệ để không trị số nào bị "đè bẹp". Gọi trung bình là $\mu$ và độ lệch chuẩn $\sigma$. Hàm chuẩn hóa $f(x)$:

**$z_i = f(x_i) = \frac{x_i - \mu_i}{\sigma_i}$**

Vector sau chuẩn hóa đưa vào ML: $\mathbf{Z} = [z_1, z_2, \dots, z_{23}]$

### 2.3. Máy học Không giám sát / KNN Similarity (Áp dụng cho AI Radio)
Sử dụng K-Nearest Neighbors (K Láng giềng gần nhất) để tính toán điểm tương đồng. Hàm tối ưu (hàm mất mát) ở đây chính là tối thiểu hóa Khoảng cách Hình học (Euclidean Distance).

Gọi $\mathbf{p}$ là bài hát đang phát (Seed), $\mathbf{q}$ là một bài hát bất kỳ trong CSDL.
Khoảng cách Euclidean $D(\mathbf{p}, \mathbf{q})$ được tính bằng:

**$D(\mathbf{p}, \mathbf{q}) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}$** *(với n = 23)*

*Logic Gợi ý:* $Queue = \underset{q \in Database}{\mathrm{argsort}} (D(\mathbf{p}, \mathbf{q}))$ (Lấy những bài hát có giá trị khoảng cách $D$ tiệm cận về $0$ nhất).

### 2.4. Phân loại theo Bầu chọn đa số (Majority Voting)
Khi chạy Nhận diện tự động, thay vì trả về khoảng cách, thuật toán lấy $K$ (ví dụ k=5) điểm gần nhất trên đồ thị đa chiều và đếm "nhãn thể loại" (Genre).

Cho $\mathcal{N}$ là tập hợp $K$ hàng xóm gần vector $x$ nhất. Nhãn thể loại của hàng xóm thứ $i$ là $y_i$. Hàm ra quyết định $y_{predict}$:

**$y_{predict} = \underset{c \in Classes}{\operatorname{argmax}} \sum_{i \in \mathcal{N}} I(y_i = c)$**
*(Hàm $I$ bằng 1 nếu mẫu $i$ có nhãn $c$, nếu không bằng 0)*

**Độ tin cậy (Confidence Score):**
Để tính tỷ lệ phần trăm chắc chắn (từ 0% đến 100%):
**$Confidence = \left( \frac{\max_{c} \sum_{i \in \mathcal{N}} I(y_i = c)}{K} \right) \times 100\%$**

Ví dụ: Nếu 4/5 bản nhạc gần nhất là EDM, độ tin cậy AI xuất ra là: $\frac{4}{5} \times 100\% = 80\%$.

---

## PHẦN 3: KIẾN TRÚC PHẦN MỀM & KỸ THUẬT (SOFTWARE ENGINEERING)

Để hiện thực hóa các công thức toán học và đáp ứng trải nghiệm người dùng ngay lập tức, dự án sử dụng các kiến trúc hệ thống chuyên biệt.

### 3.1. Sơ đồ Công nghệ (Tech Stack)
Hệ thống được thiết kế nguyên khối (Monolithic) nhưng phân lớp rõ ràng:
*   **Backend & API:** Python (FastAPI) - Xử lý API tốc độ cao, hỗ trợ bất đồng bộ (Asynchronous) hoàn hảo khi nhận File Upload.
*   **AI Engine:** Python, Librosa (Phân tích sóng âm), Scikit-learn (Model KNN), Numpy (Tính toán Ma trận).
*   **Database (CSDL):** 
    *   **Metadata:** SQLite (Lưu thông tin văn bản).
    *   **Storage Directory:** File System (Lưu trữ file `.mp3` thực tế).
    *   **Numpy Cache:** File `.npy` (Lưu trữ Vector để truy xuất siêu tốc mà không cần phân tích lại audio).
*   **Frontend:** Vanilla JavaScript, HTML5, CSS3, DOM Manipulation, Web Audio API (Trình phát nhạc tích hợp).

### 3.2. Kiến trúc Cơ sở dữ liệu (Database Schema)
Các bảng quan hệ lõi:
*   **Bảng `songs`:** Lưu trữ từng đối tượng bài hát (`id`, `title`, `artist`, `genre`, `duration`, `filepath`).
*   **Bảng `playlists`:** Quản lý danh sách phát (`id`, `name`, `created_at`).
*   **Bảng trung gian `playlist_song`:** Nơi thể hiện quan hệ Nhiều-Nhiều (N-N). Một Playlist chứa nhiều bài hát và một bài hát nằm trong nhiều Playlist. Chỉ chứa khóa ngoại: `playlist_id`, `song_id`.

### 3.3. Xử lý Đa luồng & Hiệu năng (Concurrency & Performance)
Vấn đề xảy ra khi nhiều User cùng Upload file và kích hoạt Background Task để Re-train Model AI tại cùng một thời điểm: Có thể dẫn tới xung đột ghi đè tập tin Vector Cache (`features_cache.npy`).
*   **Giải pháp - Locking:** Hệ thống sử dụng cơ chế **FileLock (`filelock`)**. Cơ chế Locking đảm bảo tính toán vẹn dữ liệu (Data Integrity). Khi một tiến trình đang nạp/lưu ma trận đặc trưng, các tiến trình khác sẽ phải vào hàng đợi (Queue), ngăn chặn hoàn toàn lỗi Corrupt file (hỏng định dạng ma trận) ở cấp độ OS.

---

## PHẦN 4: COMPLIANCE CHECKLIST (HỎI ĐÁP PHẢN BIỆN)
Dành cho bảo vệ tính khoa học của thuật toán và code.

**Q1: Tại sao lại chọn thuật toán K-Nearest Neighbors (KNN) mà không phải Deep Learning (CNN/RNN)?**
*Trả lời:* KNN không có tham số huấn luyện (non-parametric), điều này có nghĩa là khi Upload nhạc mới vào hệ thống, model cập nhật *ngay lập tức* (Lazy Learning) với chi phí $O(1)$ thay vì phải bỏ ra hàng giờ để train lại trọng số như Deep Learning. Rất phù hợp cho luồng xử lý Web thời gian thực.

**Q2: Tại sao khi bầu chọn phân loại, lại chọn $K=5$ mà không phải $K=1$?**
*Trả lời:* Việc chọn $K=5$ sinh ra cơ chế Bầu chọn Đa số (Majority Voting) nhằm giảm nhiễu cục bộ và tránh học vẹt (Overfitting). Nếu chỉ lấy $K=1$, AI sẽ dễ bị đánh lừa bởi một bài hát cùng nhịp phách nhưng sai thể loại. $K=5$ giúp mô hình ổn định và đưa ra Điểm Tự Tin (Confidence Score) đáng tin cậy.

**Q3: Nếu file nhạc người dùng tải lên bị hỏng hoặc không trích xuất được đặc trưng do lỗi định dạng thì sao?**
*Trả lời:* Backend đã xây dựng lớp ngoại lệ kế thừa `Custom Exception` kết hợp với khối `try-except` nghiêm ngặt cả trong `feature_extraction` và luồng `/analyze`. Nếu Librosa thất bại, Hệ thống ngắt phân tích, không lưu Vector hỏng, và văng mã lỗi dạng HTTP thân thiện (Fallback) về giao diện để yêu cầu người dùng thay file hoặc nhập thể loại thủ công thay vì đánh sập toàn bộ chương trình (Crash JVM/Python).
