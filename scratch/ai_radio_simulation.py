import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.datasets import make_blobs

def simulate_ai_radio_chaining():
    # 1. Tạo dữ liệu giả lập (100 bài hát)
    X, _ = make_blobs(n_samples=100, centers=5, n_features=2, random_state=42, cluster_std=1.2)
    
    # 2. Huấn luyện KNN
    k_search = 5
    nn = NearestNeighbors(n_neighbors=k_search, metric='euclidean')
    nn.fit(X)
    
    # 3. Thuật toán AI Radio Chaining
    seed_idx = 0  # Bắt đầu từ bài hát đầu tiên trong tập dữ liệu
    queue_size = 10
    
    visited = {seed_idx}
    queue = [seed_idx]
    current_idx = seed_idx
    
    # Lưu các bước di chuyển để vẽ mũi tên
    path_edges = []
    
    for _ in range(queue_size - 1):
        # Lấy các bài láng giềng của bài hiện tại
        current_point = X[current_idx].reshape(1, -1)
        distances, indices = nn.kneighbors(current_point)
        
        # Tìm bài láng giềng gần nhất mà CHƯA visited
        next_idx = None
        for idx in indices[0]:
            if idx not in visited:
                next_idx = idx
                break
        
        if next_idx is not None:
            path_edges.append((current_idx, next_idx))
            queue.append(next_idx)
            visited.add(next_idx)
            current_idx = next_idx
        else:
            # Nếu đứt xích (tất cả hàng xóm đã nghe rồi) -> dừng
            break
            
    # 4. Vẽ đồ thị
    plt.figure(figsize=(12, 10))
    
    # Vẽ toàn bộ thư viện (mờ)
    plt.scatter(X[:, 0], X[:, 1], c='lightgray', alpha=0.3, label='Thư viện nhạc', s=30)
    
    # Vẽ các bài trong hàng chờ AI Radio
    queue_points = X[queue]
    plt.scatter(queue_points[:, 0], queue_points[:, 1], c=range(len(queue)), cmap='viridis', s=100, zorder=5)
    
    # Vẽ mũi tên mô phỏng bước "Chaining"
    for start, end in path_edges:
        p1 = X[start]
        p2 = X[end]
        plt.annotate('', xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle='->', lw=2, color='blue', alpha=0.6))
        
    # Đánh dấu bài Seed và thứ tự
    plt.scatter(X[seed_idx, 0], X[seed_idx, 1], c='red', marker='X', s=200, label='Bài hát Seed (Bắt đầu)', zorder=6)
    
    for i, idx in enumerate(queue):
        plt.text(X[idx, 0] + 0.1, X[idx, 1] + 0.1, f"#{i+1}", fontsize=12, fontweight='bold')

    plt.title(f"Mô phỏng Luồng AI Radio Chaining (Nối xích {len(queue)} bài)\nThuật toán: Seed -> Sim(Seed) -> Sim(Sim(Seed))...")
    plt.xlabel("Đặc trưng 1 (MFCC)")
    plt.ylabel("Đặc trưng 2 (Tempo)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.5)
    
    save_path = "ai_radio_chaining_simulation.png"
    plt.savefig(save_path, dpi=150)
    print(f"Saved AI Radio simulation plot to: {save_path}")

if __name__ == "__main__":
    simulate_ai_radio_chaining()
