#이 코드는 시험적이며 지속적인 코드 수정이 필요

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt

# 샘플 GPS 데이터 생성 (위도, 경도)
# 실제 데이터에서는 정제된 GPS 데이터를 사용해야 합니다.
gps_train_data = np.array([
    [37.7749, -122.4194],  # 샌프란시스코
    [34.0522, -118.2437],  # 로스앤젤레스
    [40.7128, -74.0060],   # 뉴욕
    [51.5074, -0.1278],    # 런던
    [48.8566, 2.3522]      # 파리
])

# 실제 위치와 약간의 잡음이 있는 GPS 데이터를 생성
gps_train_labels = np.array([
    [37.7750, -122.4193],  # 샌프란시스코 (조정된 좌표)
    [34.0520, -118.2435],  # 로스앤젤레스 (조정된 좌표)
    [40.7127, -74.0059],   # 뉴욕 (조정된 좌표)
    [51.5075, -0.1277],    # 런던 (조정된 좌표)
    [48.8567, 2.3523]      # 파리 (조정된 좌표)
])

# KNN 모델 생성 (K=3)
knn = KNeighborsRegressor(n_neighbors=3)

# 모델 학습
knn.fit(gps_train_data, gps_train_labels)

# 새로운 GPS 데이터 (정확도를 보정하고 싶은 데이터)
new_gps_data = np.array([
    [37.7751, -122.4195],  # 샌프란시스코 근처
    [34.0521, -118.2436],  # 로스앤젤레스 근처
])

# 위치 보정
corrected_gps_data = knn.predict(new_gps_data)

# 결과 출력
for i, (original, corrected) in enumerate(zip(new_gps_data, corrected_gps_data)):
    print(f"Original GPS Data {i+1}: {original}")
    print(f"Corrected GPS Data {i+1}: {corrected}\n")

# 시각화를 통한 데이터 확인 (옵션)
plt.scatter(gps_train_data[:, 0], gps_train_data[:, 1], c='blue', label='Training Data')
plt.scatter(new_gps_data[:, 0], new_gps_data[:, 1], c='green', label='New GPS Data')
plt.scatter(corrected_gps_data[:, 0], corrected_gps_data[:, 1], c='red', label='Corrected GPS Data')
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.legend()
plt.show()
