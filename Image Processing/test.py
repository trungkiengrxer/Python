import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh và chuyển sang ảnh xám
img = cv2.imread("D:/Downloads/Sobel Img.png", cv2.IMREAD_GRAYSCALE)

# Tính gradient theo hai hướng
sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

# Tính độ lớn tổng hợp của gradient
sobel_combined = cv2.magnitude(sobel_x, sobel_y)

# Tính ngưỡng trung bình cộng
threshold_value = np.mean(sobel_combined)

# Áp dụng ngưỡng bằng trung bình cộng
_, sobel_thresh = cv2.threshold(sobel_combined, threshold_value, 255, cv2.THRESH_BINARY)

# Hiển thị kết quả
plt.figure(figsize=(10,5))
plt.subplot(1, 3, 1), plt.imshow(img, cmap='gray'), plt.title('Ảnh gốc')
plt.subplot(1, 3, 2), plt.imshow(sobel_combined, cmap='gray'), plt.title('Độ lớn Gradient')
plt.subplot(1, 3, 3), plt.imshow(sobel_thresh, cmap='gray'), plt.title('Ảnh Biên (Ngưỡng trung bình)')
plt.show()
