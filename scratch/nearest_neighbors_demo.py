import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.datasets import make_blobs
import os

def simulate_nearest_neighbors():
    # 1. Tạo dữ liệu giả lập (2D để dễ hình dung)
    # Giả sử đây là các bài hát đã được trích xuất MFCC và Tempo
    X, y = make_blobs(n_samples=50, centers=3, n_features=2, random_state=42, cluster_std=1.0)
    
    # 2. Khởi tạo và huấn luyện NearestNeighbors
    # Trong dự án AIRadio, chúng ta dùng K=7
    k = 7
    # Dùng cosine metric như trong dự án thực tế
    # Lưu ý: Với cosine, dữ liệu thường được chuẩn hóa, ở đây ta dùng Euclidean để minh họa trực quan trên đồ thị
    nn = NearestNeighbors(n_neighbors=k, metric='euclidean')
    nn.fit(X)
    
    # 3. Chọn một "Bài hát đang phát" (Test Point)
    test_point = np.array([[0, 0]])
    distances, indices = nn.kneighbors(test_point)
    
    # 4. Vẽ đồ thị
    plt.figure(figsize=(10, 8))
    
    # Vẽ tất cả bài hát trong Database
    plt.scatter(X[:, 0], X[:, 1], c='gray', alpha=0.5, label='Bài hát trong Database', s=50)
    
    # Vẽ các bài hát "Hàng xóm" được chọn cho AIRadio
    neighbor_points = X[indices[0]]
    plt.scatter(neighbor_points[:, 0], neighbor_points[:, 1], c='blue', edgecolors='k', s=100, label=f'{k} bài hát tương đồng nhất')
    
    # Vẽ bài hát đang phát (Seed Song)
    plt.scatter(test_point[:, 0], test_point[:, 1], c='red', marker='X', s=200, label='Bài hát đang phát (Seed)')
    
    # Vẽ các đường nối từ Seed tới các Neighbors để minh họa khoảng cách
    for point in neighbor_points:
        plt.plot([test_point[0, 0], point[0]], [test_point[0, 1], point[1]], 'r--', alpha=0.3)
    
    plt.title(f"Mô phỏng thuật toán NearestNeighbors (K={k})\n(Cơ chế hoạt động của AI Radio)")
    plt.xlabel("Đặc trưng 1 (VD: MFCC Mean)")
    plt.ylabel("Đặc trưng 2 (VD: Tempo)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Lưu file
    save_path = "nearest_neighbors_simulation.png"
    plt.savefig(save_path, dpi=150)
    print(f"Saved simulation plot to: {save_path}")

if __name__ == "__main__":
    simulate_nearest_neighbors()
