import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.datasets import make_blobs
import os

def simulate_radius_neighbors():
    # 1. Create synthetic data (2D for visualization)
    X, y = make_blobs(n_samples=100, centers=3, n_features=2, random_state=42, cluster_std=1.5)
    
    # 2. Init and train RadiusNeighborsClassifier
    radius = 5.0
    clf = RadiusNeighborsClassifier(radius=radius, outlier_label='most_frequent')
    clf.fit(X, y)
    
    # 3. Create meshgrid for decision boundaries
    h = .1  # step size in the mesh
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # 4. Plot
    plt.figure(figsize=(10, 8))
    
    # Plot decision boundaries
    plt.pcolormesh(xx, yy, Z, alpha=0.1, cmap='viridis')
    
    # Plot original data points
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap='viridis', s=50)
    plt.legend(*scatter.legend_elements(), title="Genres")
    
    # 5. Simulate Radius at a specific point
    test_point = np.array([[0, 0]])
    prediction = clf.predict(test_point)
    plt.scatter(test_point[:, 0], test_point[:, 1], c='red', marker='X', s=200, label='Test Point')
    
    # Draw circle of radius R around test point
    circle = plt.Circle((test_point[0, 0], test_point[0, 1]), radius, color='red', fill=False, linestyle='--', label=f'Radius R={radius}')
    plt.gca().add_patch(circle)
    
    plt.title(f"RadiusNeighborsClassifier Simulation (Radius = {radius})\nRed point predicted as Genre: {prediction[0]}")
    plt.xlabel("Feature 1 (e.g. Tempo)")
    plt.ylabel("Feature 2 (e.g. MFCC Mean)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Save file
    save_path = "radius_neighbors_simulation.png"
    plt.savefig(save_path, dpi=150)
    print(f"Saved simulation plot to: {save_path}")

if __name__ == "__main__":
    simulate_radius_neighbors()
