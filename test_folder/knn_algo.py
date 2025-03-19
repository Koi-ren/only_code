import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt

# 샘플 GPS 데이터 생성 (위도, 경도)
gps_data = np.array([
    [37.7749, -122.4194],  # 샌프란시스코
    [37.7750, -122.4193],
    [37.7748, -122.4192],
    [37.7752, -122.4195],
    [40.0000, -120.0000],  # Outlier (튀는 값)
    [37.7749, -122.4194],  # 샌프란시스코
])

# 튀는 값(Outlier)을 식별하는 간단한 방법 (거리 기반)
def detect_outliers(data, threshold=0.001):
    diffs = np.sqrt(np.sum(np.diff(data, axis=0)**2, axis=1))
    outlier_indices = np.where(diffs > threshold)[0] + 1
    return outlier_indices

outlier_indices = detect_outliers(gps_data)

# KNN 모델 생성 및 학습
knn = KNeighborsRegressor(n_neighbors=3)
# 튀는 값을 제외한 정상적인 데이터를 사용하여 학습
knn.fit(np.delete(gps_data, outlier_indices, axis=0), np.delete(gps_data, outlier_indices, axis=0))

# 튀는 값을 KNN으로 보정
gps_data_corrected = gps_data.copy()
gps_data_corrected[outlier_indices] = knn.predict(gps_data[outlier_indices])

# 결과 출력
print("Original GPS Data:")
print(gps_data)
print("\nCorrected GPS Data:")
print(gps_data_corrected)

# 시각화
plt.plot(gps_data[:, 0], gps_data[:, 1], 'ro-', label='Original GPS Data')
plt.plot(gps_data_corrected[:, 0], gps_data_corrected[:, 1], 'bo-', label='Corrected GPS Data')
plt.scatter(gps_data[outlier_indices, 0], gps_data[outlier_indices, 1], c='red', label='Detected Outliers')
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.legend()
plt.show()
