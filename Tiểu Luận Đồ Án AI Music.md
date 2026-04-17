# **TIỂU LUẬN ĐỒ ÁN**

**TÊN ĐỀ TÀI: XÂY DỰNG HỆ THỐNG TRÌNH PHÁT ÂM NHẠC TÍCH HỢP TRÍ TUỆ NHÂN TẠO \- ỨNG DỤNG MACHINE LEARNING TRONG PHÂN LOẠI THỂ LOẠI VÀ ĐỒNG BỘ LỜI BÀI HÁT TỰ ĐỘNG.**

## **CHƯƠNG 1: TỔNG QUAN DỰ ÁN VÀ ĐẶT VẤN ĐỀ**

### **1.1. Bối cảnh và Đặt vấn đề**

Trong kỷ nguyên âm nhạc số, người dùng không chỉ dừng lại ở việc nghe nhạc mà còn đòi hỏi trải nghiệm tương tác cao (như xem lời bài hát khớp từng giây) và hệ thống gợi ý thông minh. Tuy nhiên, quy trình quản lý nhạc số truyền thống đang gặp phải các điểm nghẽn lớn, đặc biệt là các **Vấn đề về Dữ liệu (Data Issues)**:

1. **Sự giao thoa và mập mờ trong nhãn dữ liệu (Genre Overlap):** Ranh giới giữa các thể loại nhạc hiện đại không còn rõ ràng. Một bài Rap có thể có nhịp điệu rất chậm như Ballad, hoặc một bài Pop có thể phối khí điện tử chói tai như EDM. Việc gán nhãn thủ công (metadata) vừa tốn kém nhân sự vừa mang tính chủ quan cảm tính cao, dễ dẫn đến sai lệch trong hệ thống gợi ý.  
2. **Độ nhiễu của dữ liệu âm thanh:** Các file audio tải lên thường không đồng nhất. Có bài hát chứa đoạn nhạc dạo (intro) dài hàng chục giây không lời, hoặc chứa nhiều tạp âm. Điều này gây khó khăn lớn cho các mô hình nhận diện giọng nói (Speech-to-Text).  
3. **Chi phí tạo Lời bài hát đồng bộ (Synchronized Lyrics):** Việc tạo file LRC thủ công yêu cầu con người phải nghe và gõ tọa độ thời gian chính xác đến từng mili-giây cho từng câu hát. Đây là quy trình đắt đỏ và không thể mở rộng (scale) khi số lượng bài hát lên tới hàng ngàn bài.

Dự án này ra đời nhằm giải quyết triệt để bài toán: **Tự động hóa hoàn toàn quy trình xử lý nhạc bằng AI**, từ việc phân tích bản chất vật lý của giai điệu để phân loại thể loại, cho đến việc tự động "nghe" và viết lại lời nhạc đồng bộ.

### **1.2. Mục tiêu dự án**

* **Tự động hóa trích xuất đặc trưng:** Sử dụng thuật toán xử lý tín hiệu số (DSP) để hiểu "Dấu vân tay âm thanh" của mỗi bài hát.  
* **Hệ thống phân loại thông minh:** Ứng dụng K-Nearest Neighbors (KNN) phân loại nhạc dựa trên dữ liệu sóng âm thay vì cảm tính con người.  
* **Đồng bộ lời nhạc bằng AI:** Tích hợp mô hình OpenAI Whisper để tự động bóc băng (Speech-to-Text) và tạo file LRC chuẩn xác.  
* **Trải nghiệm người dùng cao cấp:** Xây dựng giao diện UI/UX hiện đại, tối ưu cho việc thưởng thức nội dung (visual-centric) kèm khả năng chỉnh sửa linh hoạt.

## **CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ**

### **2.1. Phân tích Đặc trưng Âm thanh (Audio Feature Extraction)**

Để máy tính "hiểu" được âm nhạc, hệ thống không dùng các lệnh IF-THEN cứng nhắc (ví dụ: If BPM \< 100 then Vpop). Thay vào đó, thuật toán sẽ trích xuất một **vector 23 chiều** cho mỗi bài hát (code tại src/audio\_processing/feature\_extraction.py).

Dưới đây là ý nghĩa vật lý và các bảng khung giá trị (tham chiếu tương đối) của các đặc trưng quan trọng nhất:

**2.1.1. Nhịp độ (Tempo / BPM)**

Trích xuất bằng librosa.beat.beat\_track. Đây là "nhịp tim" của bài hát, đo lường tốc độ nhịp điệu.

*Bảng 1: Phân loại theo Tempo (Độ Vận Tốc \- BPM)*

| Khoảng BPM | Đặc tính nhịp điệu | Thể loại biểu diễn tiêu biểu | Ví dụ tham khảo |
| :---- | :---- | :---- | :---- |
| **\< 80 BPM** | Rất chậm, buồn, du dương | Ballad, Lo-fi chill, Acoustic | *Rất chậm* |
| **80 \- 110 BPM** | Chậm vừa phải, có nhịp rưỡi | Pop buồn, Old-school Rap âm hưởng lofi | *Lối Nhỏ (92), Chìm Sâu (103)* |
| **110 \- 130 BPM** | Nhịp điệu tiêu chuẩn, vui tươi | Pop tiêu chuẩn, R\&B, Trap | *Sugar (117)* |
| **130 \- 150 BPM** | Cực kỳ sôi động, nhún nhảy | Rap/Trap dập mạnh, EDM | *Tại Vì Sao (136), Mang Tiền Về (136)* |

**2.1.2. Trọng tâm phổ (Spectral Centroid \- Hz)** Đo lường độ "sáng" của âm điệu. Số Hz càng thấp thì nhạc càng ồm/trầm/nhiều bass. Số càng cao thì nhạc càng réo rắt/chói (nhiều tiếng Treble, Synth, Vocal cao).

*Bảng 2: Phân loại theo Spectral Centroid (Độ Sáng / Chói)*

| Khoảng Tần số | Đặc tính âm thanh | Thể loại thường thấy | Ví dụ |
| :---- | :---- | :---- | :---- |
| **\< 1500 Hz** | Âm thanh tối, rất sâu, u buồn | Lo-fi, Piano cover, Ballad trầm |  |
| **1500 \- 2000 Hz** | Sáng vừa phải (Trọng tâm Vocal) | Indie, Pop nhẹ, Rap có giai điệu thư giãn | *Lối Nhỏ (1740 Hz), Chìm Sâu (1918 Hz)* |
| **\> 2000 Hz** | Rất chói, sáng (Nhiều Synthesizer) | Pop năng động, Electro Rap, EDM | *Sugar (2171 Hz), Tại Vì Sao (2408 Hz)* |

**2.1.3. Tỷ lệ qua không (Zero-Crossing Rate \- ZCR)** Đo mức độ ma sát, tiếng trống nảy (Snare), tiếng hi-hat. Nhạc nào đập bùm chát mạnh và nhiễu thì số này sẽ cao.

*Bảng 3: Phân loại theo Zero-Crossing (Độ "Gắt", Nhiễu)*

| Dải ZCR | Mức độ Gắt (Cấu trúc nhịp gõ) | Thể loại thường thấy | Ví dụ |
| :---- | :---- | :---- | :---- |
| **\< 0.050** | Sạch sẽ, mượt mà | Nhạc không lời, Acoustic gảy đàn |  |
| **0.050 \- 0.080** | Gõ nhịp lưa thưa, trống nhẹ | Rap tiết tấu lững lờ | *Lối Nhỏ (0.060), Chìm Sâu (0.077)* |
| **0.080 \- 0.100** | Trống dập có lực, dòn, vang | Pop chuẩn, Rap Oldschool/Trap | *M.T.V.C.M (0.081), Sugar (0.092)* |
| **\> 0.100** | Cực gắt, ồn ào, gai góc | EDM, Rock, Metal |  |

**2.1.4. 20 Hệ số MFCC (Mel-Frequency Cepstral Coefficients)** Đây là 20 chiều dữ liệu quan trọng nhất, dùng để phân tích âm sắc, chất giọng ca sĩ (Timbre / Vocal), mô phỏng cách màng nhĩ con người cảm nhận âm thanh.

### **2.2. Thuật toán K-Nearest Neighbors (KNN)**

Thay vì dùng luật IF-THEN trên các bảng trên, AI sẽ gom toàn bộ 23 con số lại, căn chỉnh tỷ lệ (Scale) thông qua StandardScaler.

Trong không gian 23 chiều, mỗi bài hát là một điểm tọa độ. Mô hình áp dụng **Cosine Similarity** (metric="cosine") để tính góc tương đồng giữa các vector, từ đó tìm ra ![][image1] điểm lân cận gần nhất để quyết định thể loại của một bài hát mới.

### **2.3. Mô hình Ngôn ngữ OpenAI Whisper**

* **Cơ chế (ASR):** Sử dụng phiên bản **Whisper base** (src/audio\_processing/whisper\_service.py), ứng dụng kiến trúc Transformer chuyển đổi tín hiệu âm thanh trực tiếp sang văn bản (End-to-End).  
* **Định dạng LRC:** Trích xuất start\_time của từng phân đoạn và format thành chuỗi chuẩn \[mm:ss.xx\] Text (Ví dụ: \[01:15.83\] Lời bài hát), cung cấp dữ liệu gốc cho trình phát nhạc UI hiển thị.

## **CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG**

### **3.1. Kiến trúc Hệ thống (System Architecture)**

Hệ thống được thiết kế theo mô hình Microservices:

* **AI Engine (Python/FastAPI):** Đảm nhiệm các tác vụ tính toán nặng (trích xuất Feature, chạy model KNN và chạy Whisper).  
* **Backend (Spring Boot/NodeJS):** Quản lý luồng nghiệp vụ, API RESTful và thao tác với Database.  
* **Cơ sở dữ liệu:** Lưu trữ tập trung. Bảng songs chứa đặc trưng âm thanh và trường lrc\_content dạng TEXT lưu cấu trúc lời bài hát đã được đồng bộ hóa.

### **3.2. Thiết kế Giao diện và Trải nghiệm (UI/UX)**

Logic Frontend (src/frontend/lyric\_player.js) bám sát tiêu chuẩn của các nền tảng thương mại:

* **Slide-in Panel:** Panel lời nhạc trượt lên (Overlay) mượt mà từ góc phải, đè lên danh sách gợi ý mà không làm gián đoạn bối cảnh trình phát.  
* **Dynamic Blurred Background:** Tự động lấy ảnh bìa (Album Art), áp dụng CSS filter: blur() brightness() làm nền, giúp giao diện thay đổi linh hoạt theo từng bài hát.  
* **Auto-scroll (Kinetic Scrolling):** Tính toán bù trừ chiều cao màn hình (offset \= (viewportHeight \* 0.45) \- lineOffsetTop) để luôn giữ câu hát hiện tại ở vùng trung tâm thị giác.

### **3.3. Giải pháp "Human-in-the-loop" (Con người làm trung tâm)**

Hệ thống ứng phó linh hoạt với các lỗi AI (nghe nhầm tiếng lóng, sai thời gian intro):

* **Cơ chế Quick Edit (Sửa nhanh):** Cung cấp giao diện Textarea font Monospace. Người dùng/Admin có thể nhấn biểu tượng bút chì để sửa trực tiếp file LRC gốc. API PUT /songs/{id}/lyrics sẽ cập nhật dữ liệu Real-time.  
* **Validate dữ liệu an toàn:** Áp dụng Regex /\\\[\\d{2}:\\d{2}\\.\\d{2,3}\\\]/ ngay tại Frontend để ngăn chặn việc người dùng vô tình xóa mất định dạng thời gian của thẻ LRC, bảo vệ hệ thống khỏi lỗi crash.

## **CHƯƠNG 4: TRIỂN KHAI VÀ ĐÁNH GIÁ THỰC NGHIỆM**

### **4.1. Tối ưu hóa Dữ liệu và Siêu tham số**

* **Kích thước Dataset:** Khởi điểm với 54 quan sát, dự án đã thu thập và mở rộng lên **64 bài hát** đại diện cho 5 nhãn thể loại nhằm cân bằng phân bố lớp dữ liệu.  
* **Tối ưu K trong KNN:** Áp dụng quy tắc toán học ![][image2] (với ![][image3], suy ra ![][image4]). Dự án chọn cấu hình n\_neighbors \= 7 (số lẻ để Majority Voting không bị hòa). Việc nâng cấp từ K=5 lên K=7 giúp mô hình giảm nhiễu (variance) và phân loại ổn định hơn ở các vùng ranh giới âm thanh giao thoa.

### **4.2. Khắc phục nhiễu dữ liệu: Thuật toán Tịnh tiến thời gian**

Trong quá trình thực nghiệm OpenAI Whisper, một vấn đề lớn phát sinh là các đoạn nhạc dạo (Intro) kéo dài không lời khiến toàn bộ trục thời gian bị lệch (Ví dụ: Ca khúc *Nơi này có anh* lệch 7 giây, sau đó tinh chỉnh thành 6 giây, và chốt ở mức lệch 13 giây so với bản gốc).

* **Giải pháp thực nghiệm:** Tích hợp logic tịnh tiến thời gian tuyến tính (Time-shifting) vào luồng Quick Edit. Hệ thống cho phép cộng/trừ một hằng số ![][image5] vào toàn bộ các mốc \[mm:ss.xx\] trong ma trận LRC. Điều này giải quyết triệt để vấn đề lệch nhịp mà không cần phải chạy lại toàn bộ model AI đắt đỏ.

## **CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN**

### **5.1. Kết quả đạt được**

Đồ án đã giải quyết trọn vẹn bài toán đặt ra: Xây dựng thành công một Hệ thống Trình phát nhạc thông minh. Hệ thống không chỉ có khả năng lưu trữ, phát nhạc cơ bản mà còn sở hữu "bộ não" phân tích sóng âm đa chiều. Việc kết hợp thành công KNN trong phân loại và Whisper trong tạo file LRC đã giúp tự động hóa hoàn toàn luồng quản lý dữ liệu, đồng thời cung cấp trải nghiệm UI/UX tiệm cận với các nền tảng công nghiệp.

### **5.2. Hướng phát triển tương lai**

* **Nâng cấp thuật toán AI:** Nghiên cứu chuyển đổi từ mô hình KNN sang Deep Learning (sử dụng Mạng nơ-ron tích chập \- CNN trên ảnh phổ Mel-spectrogram) để tăng khả năng học các biểu diễn âm thanh phức tạp.  
* **Syllable-sync Lyrics:** Nâng cấp cấu trúc file LRC để hỗ trợ đồng bộ hiển thị làm sáng từng âm tiết (chữ cái) tương tự cách Spotify đang vận hành, thay vì chỉ làm sáng toàn bộ một dòng (Line-by-line).

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAYCAYAAAD3Va0xAAABN0lEQVR4Xu2SP0vDQBiHU4qg2EUhBmOSS0wW50yOTuLSRYdCly79En4FB0FcRT+Eg4ODkyAOji4ugtDJxcFBEX3eegdvzzjZzf7gIXfvnx937yUI/o3aZVmuGGNWNWEYdlxBXddzRVFEOp/n+bw2CZIkWc6ybI/kHTwKFA1oNK6mqqqQ+DU8wL5A35r2GQujJZK3cCSoVEvAuEfNkHVb5X6KohqDlzRNu4LEoihaJHZg2fJ7GjU1Iwr78AwbAlfJ+Z7IV+TX/6YWJzql8cqdyHwP/V5eSvAbGqUGPZKhWrbZv7u939MoNx/YdTGedoH4hUP2uqdRUzOygx7RsK7jciXir5ZNnfM1/tnsoC/luXWSWAFPlmNbPykSOxjcCKw/4I31mXsle7VDmxM+4TyO49T3mmmmv+oL32BdUR57j/wAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE0AAAAYCAYAAAC/SnD0AAADuUlEQVR4Xu2YS2hTQRSGJ31IRakaTWObJpOkdWHRhWRRFIUq4gNRRF2olepGKL7rRnBRi4rgW7QoLqQKgo+lCIq4KAiitKAb7UYXglgQRHDhoiLx/zszdjK5N0nbTWjvDx/35pwzr3Pn1QoxfRSKxWIdJJFInJsMbsVTVul0eg4GfIrgZzWomgTTQ0HSxq8QknUCS3M+cZ2TVWVTU1OdlLLeJhKJzKYzk8lUk1QqFTW+ZDJZQ9yKykno30L09QxeQxpjn2uP02MceflgmZyIxsbGML7IDjjfgS8EQfuQJEl/c3NzhMD+GnwCJ1EmRnIqKjNhTOeZOMdcBVsbxnBFkwW9wkoq8wHbQfAV3CCwLbXqUEID8+AcANeJ5QqhkZ0EMfvxu9Lyla2i0Wgd+ntLWMmwxQ9PEPNQJydl+xsaGhbAdqngigqSNrGkZRD0Kx6PbyG0oeFZsF0Eq4lbppi4JxLuhdwTXb9RS0vLDCJ8BjgRJdTdKu3aKfYJ4zmrWQF+gkN2DPOBZHXatjyhUDv4ARYTFEjieYdPN7YEcXZ2STVzB/B+D8+PeO4Saqbas5WxnYQfybIXkm9yuR/pPfqC8InTYzxO8LMKzwfgDa8nhDEo3wFWOkVzxKO5DwX7zUyT6kAY4ixxg4sJ5VJIwl6Re2pVwr4b9hcEbaziQYN2u8FhYlXhqXA4XEtQz02pTsU8wX6aIHGtrs8IbW028Df6swFlRvgkQn3InoIHXWJsPxtO6v0LrMfvP3x344sJ5er9GjR3Jqn2FA5+k8iffZ5C7GXNffANpgrbry+yT4jwmWUU/EdAmvC3Xq79Us04wmsGP4r/hTZI2sSSNnoIgO3GhkHPhP054TuxyxSTPn3MIAfBAb868GHaNN6n1JhGlzsHi/qyeHIL+C8sed4fWwstTXMImEPK2Dk5YP9NUO/RZImHwLDJvJFV0XJi+wpJd6wX5VuJVF9uG3gG1hChZwIvzYjpIsZWgioQ/xj1fOC7Af1/JHL30TxJfQi4du7dsA9pmAvfQ8B8uT4EvnRPL9hSUt1heomOLyrELpMeVxQkqBZtXSPwv5dqSQxiZiwibnwhIb4NZbOYXesI6jwG1rpxrnjIIeFbXTsFew9BvZ+ZRNfPgW1EI28J3v+CEbzfZTDRy/Oq9mU1T7Hs4m5dHir6XwF0roZ/34kS9jIfhXTiXxFrluUpqcX+6/F8l2p1tdtxSOgSgtDbwqv/Mkja+JM2FYRE7TEftJSlGUiJ+3E34bvrDBQoUKBA/voHhjpEmPAPNaIAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAYCAYAAABN9iVRAAACnUlEQVR4Xu2XO2hUQRSG75IVFHzjKu5r7j5gCQgWW9ikTKGYiIigoARMIRLEMoUaEdIIIlj4QiNioSms01lYBUUQrBQtRJC0QsDGIvj9d2fi7LCaFfRi2PvDx517zpnHmdfejaJMmQZeQ41GY7cxZq+eQjbnjON4o5Df4WxeG/+rhlqt1pbQuKpyubyTRI6S1CKsCN4POj/vw6Jard7l+RmmisXiLuG386/FODcJxnGFMSzAU8pnBe5cGC/hOw2PQnuXlAiN3YE3lnnMeT+GRkaxT/q2tNRutzfQ/z3LNKYcY7kMH0WtVtsT1mGimviWWMjHoa9LNNgm6BzB5y1fK5XKPj9GfsX5trSknciY3gqXKLYDcEZoclysygL7VeKfZ8n/TiQ1ASME1yxfVFm++OeFN0vMjqBqGsrp3JrOOV/QovB+nEnYL59lVYz1hCBmXImvlXxOiXJGSioLOrkF7zTLsgs7GT0vFl+m84twA+73A4O8IKLgjnEqFAqbiXtBzAfLWLPZ3IrtAeVpEdlx2XM+I3jNr5m8VpPgS5HXubY3tmUqnqQ8KjSbXrXU5JKH18LtPo2J9yXLsLY6z4ulUqksFNNP8sl5D8x5GpqHl2pQKC6ISUVe8k9EZFfZLtA3QXmc43CE8qTxvkfgmej1/ZJo0JOfgJEuY5RsGd2w323HOnN9XXb2a/G66XG+f8GUiMKBecI/Z3onv2w5ZAnb/iSIvSbIabtr011us+6M+KrX69tMZ+XV8VzoT1N2IfQFuugWgfIxYz9y+EirhHWknmeeBsao9N6ywvsrbvZWV1CUdKDf/FMi9KUpe5ndFoz1ph2TduRh4cfGVqZzbLVzxUPhr/x6U7JTlZiOabw+/lj9NQ108pkyZcqU6U/0Aztt9euitKBXAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEcAAAAXCAYAAABZPlLoAAADT0lEQVR4Xu2YS2hTQRSGb19Q8VGKxjRtk5ukgSIKCsEXKOJCsAtF2oVVobiyKOJjUVREcFFEW4ooiqIVqdAK6lI3uhF0pxsXLl1U7UoXKrgQlfr9N3PrdEhs+qJW88PHzD1z5nUyZ24Sz5uGGhsbWxOJxLmZQGMJd475qnLf97spqwyV06Tc8E+oFJxCisfjB0mDjGv/7xWNRhdyT1ykWua2TVbNzc2LKSpc+7wV6dQVi8VWOOYy7C3JZPKxYYDnK+l0usbxC6RTJ/B5BjG3fbaVzWarWOMxwfxDcB969MEL178YBfcCg/R5zqnB1gaPFAzBpBt4/qKA2X6SWdg9QfvwXASHuds5/R3Csu1mLb3Cm0JWlIJTSAx01LAytKVSqahgwFcMvj20ZzKZCM/HoS60hdIiGOOamKvgMGc/69gvQhvryfq5FBvCXm25Byprampa7hqNyul8XXhWVHlr7RQM+AE20r7DsI07ZYHVP5C5Z85Aq2FOgsPmO5n3p6B+UvcM5Sme9wrbN0yXW3DHy3Ok2GwnG1svHPsJQb+vDH6WE7NEUN/jmzQLfZVO2LobGhoawyAWGZxKfI/gd6NI+gwFxzVv3NsCv1H4AV1ebu/j9l8KTqHgyChwvCxHyvRYY05B4Dy3ozcuON8pN4X2+vr6Zdhe6/iGNuq7fHNBTzI4My7WUse8dwX1C5Sf/VyaHRaetc9g07W1tTU0fGLRPZ71dZ7nDu6VtaGzLSs473UiQnskElmE7SkTDxCouMDvvEoFQ2MK6iNc6Kvxqxb22LOoSubtZ0+bhQzmtA+wpreC9pTbSZvtoeGj9WVIp+aqlyfVJNpaDMP5gqNFJH/rkm+OftJ8WaT+DQaprxH22JYq8DkU9i2C4HVc6OVCW8zPrU3l2Kll77U8PxHUs3afQAQk5edSKzwRbWx6q+sXSq9xgd/LhJVWChS2N5D3b4jEHKaV7kHmfMipWSVCO2tein1QaE92n0Cl4PwhOBKNN+GdQSk14V8JCoJJlXbBcz/06g1l+9FWjf00jBhG4cUEaTXj0l3DvM8FH9IByn3wwDfXhOs/JuWbWbQoeGpcmZ8NW0TByP9F0gclWOs6obrrk1dKEZMmeS/ikkoqqaQp6BfVu0XROX8SxgAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAYCAYAAAARfGZ1AAABa0lEQVR4Xu2Tv0oDQRDG9ySCkk6Fk/t/YmdA5GwsfIVU+gw+QQqtFA1WEQutFKxE8Bms4wuITyA2FlYWVvp9ycyxbg4hkqvMBz9yOzOZ+3Z2z5ipxlEcx5skTdNuURSzbv7PYrMsy+4Jmn+CLbemQh7qNnzfbxI3WQqOt1F4JbyAO4QbQqWSJFlB3TN+C+LmVQ0UnUVRtErg/lDd/7YDGGoj/xQEwRJx86r6mrMBGu7j0SNY5zoaazwD4eUhwRh2kLsFfT4T9Fgum4pK13ZQ3H8Qe56IzxHWI/cIOnme+2TkhsnWT8zQdSn586twbZyDtQ/TjqsGNwHJU7DmJs1wPMfCD/eUPW87rqqvud5NzO/IOCNR8aUETd7AhbHqsO4id8OYfkQ6c7rqCQd62hXsEtT0wTvctrQR1g8wtoezmefhkzAMF7mlFouFrzGg+xmCl55jfQl6uCnrRHc1CXlwvTBy/SakWptP9R/0DaB4fFsrfAh3AAAAAElFTkSuQmCC>