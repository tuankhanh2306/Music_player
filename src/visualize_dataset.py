import os
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import settings

def load_data():
    """Tải dữ liệu từ Database (lấy nhãn Genre) và Cache (lấy Vector)"""
    # 1. Tải Cache Vector
    cache_path = settings.FEATURE_CACHE_PATH
    if not os.path.exists(cache_path):
        print(f"❌ Không tìm thấy file cache: {cache_path}")
        return None, None

    try:
        feature_cache = np.load(cache_path, allow_pickle=True).item()
    except Exception as e:
        print(f"❌ Lỗi đọc cache: {e}")
        return None, None

    # 2. Truy vấn Database lấy Thể loại
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if not os.path.exists(db_path):
        # Fallback thử đường dẫn local
        db_path = "music_db.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, genre FROM songs")
    songs = cursor.fetchall()
    conn.close()

    # 3. Kết hợp Dữ liệu
    dataset = []
    for song_id, title, genre in songs:
        if song_id in feature_cache and genre:  # Chỉ lấy bài hát ĐÃ CÓ vector và ĐÃ CÓ thể loại
            vector = feature_cache[song_id]
            # Bóc tách 3 thông số đặc biệt nằm ở cuối vector 23 chiều: 
            # Index 20: Tempo, Index 21: Centroid, Index 22: ZCR
            if len(vector) == 23:
                dataset.append({
                    'id': song_id,
                    'title': title,
                    'genre': genre.strip(),
                    'tempo': vector[20],
                    'centroid': vector[21],
                    'zcr': vector[22]
                })

    print(f"✅ Đã tải thành công {len(dataset)} bài hát có đủ nhãn và vector từ dataset gốc.")
    return dataset

def plot_2d_scatter(dataset):
    """Vẽ biểu đồ phân tán 2D: Tempo vs Spectral Centroid"""
    if not dataset:
        return

    # Chuẩn bị dữ liệu vẽ
    genres = list(set([d['genre'] for d in dataset]))
    
    plt.figure(figsize=(10, 6))
    
    # Thiết lập màu sắc (dùng seaborn palette)
    colors = sns.color_palette("husl", len(genres))
    color_map = {genre: colors[i] for i, genre in enumerate(genres)}

    # Vẽ từng điểm
    for d in dataset:
        plt.scatter(
            d['tempo'], 
            d['centroid'], 
            color=color_map[d['genre']], 
            alpha=0.7,
            edgecolors='w',
            linewidth=0.5
        )

    # Thêm Legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', label=g,
                          markerfacecolor=color_map[g], markersize=10) for g in genres]
    plt.legend(handles=handles, title="Thể loại (Genre)")

    # Gán nhãn Label
    plt.title("Biểu đồ Phân tán: Vận tốc (BPM) vs Độ sáng (Spectral Centroid)")
    plt.xlabel("Tempo (BPM)")
    plt.ylabel("Spectral Centroid (Hz)")
    plt.grid(True, linestyle='--', alpha=0.5)

    # Lưu lại
    out_file = "dataset_2d_scatter.png"
    plt.savefig(out_file, dpi=300)
    print(f"📸 Đã lưu biểu đồ 2D tại: {out_file}")

def plot_3d_scatter(dataset):
    """Vẽ biểu đồ phân tán 3D: Tempo, Centroid, ZCR"""
    if not dataset:
        return

    genres = list(set([d['genre'] for d in dataset]))
    colors = sns.color_palette("husl", len(genres))
    color_map = {genre: colors[i] for i, genre in enumerate(genres)}

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for d in dataset:
        ax.scatter(
            d['tempo'], 
            d['centroid'], 
            d['zcr'], 
            color=color_map[d['genre']], 
            alpha=0.8,
            s=40
        )

    # Thêm Legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', label=g,
                          markerfacecolor=color_map[g], markersize=10) for g in genres]
    ax.legend(handles=handles, title="Thể loại")

    ax.set_title("Không gian Đặc trưng 3D của Dataset")
    ax.set_xlabel("Tempo (BPM)")
    ax.set_ylabel("Spectral Centroid (Hz)")
    ax.set_zlabel("Zero-Crossing Rate (ZCR)")

    out_file = "dataset_3d_scatter.png"
    plt.savefig(out_file, dpi=300)
    print(f"📸 Đã lưu biểu đồ 3D tại: {out_file}")

if __name__ == "__main__":
    print("⏳ Bắt đầu trích xuất và visualize dataset...")
    data = load_data()
    if data and len(data) > 0:
        # Sử dụng seaborn style cho biểu đồ đẹp mắt hơn
        sns.set_theme(style="whitegrid")
        
        plot_2d_scatter(data)
        plot_3d_scatter(data)
        print("🎉 Hoàn tất!")
    else:
        print("⚠️ Không có đủ dữ liệu. Hãy đảm bảo bạn đã import bài hát và cập nhật vào DB/Cache.")
