import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt # Cần cài đặt: pip install matplotlib

def show_me_the_matrix():
    # 1. Tạo một âm thanh giả lập (tần số 440Hz - nốt La) trong 2 giây
    sr = 22050
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration))
    y = 0.5 * np.sin(2 * np.pi * 440 * t) 

    # 2. Trích xuất ma trận MFCC (chưa lấy mean)
    # Kết quả mfcc ở đây là ma trận 2D: (số đặc trưng x số khung thời gian)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)

    print(f"--- THÔNG TIN MA TRẬN ---")
    print(f"Shape: {mfcc.shape} (20 dòng đặc trưng, {mfcc.shape[1]} cột thời gian)")
    print(f"\nMột phần dữ liệu của ma trận (5x5):")
    print(mfcc[:5, :5]) 

    # 3. Vẽ ma trận này ra thành hình ảnh (Heatmap)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfcc, x_axis='time', sr=sr)
    plt.colorbar()
    plt.title('Ma trận MFCC (Âm thanh nốt La)')
    plt.tight_layout()
    
    # Lưu ra file ảnh để xem
    output_path = "mfcc_visualization.png"
    plt.savefig(output_path)
    print(f"\n✅ Đã lưu hình ảnh minh họa ma trận tại: {output_path}")
    print("Mẹo: Vector đặc trưng dùng cho AI chính là giá trị trung bình của mỗi dòng trong ma trận này.")

if __name__ == "__main__":
    show_me_the_matrix()
