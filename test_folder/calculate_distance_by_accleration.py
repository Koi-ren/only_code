import numpy as np

# 샘플링 시간 간격 (초)
dt = 0.01  # 100Hz 샘플링

# 가속도 데이터 (IMU로부터 얻은 x, y, z축 가속도 값)
# 예시로 간단하게 100개의 가속도 데이터를 생성
accel_data = {
    'x': np.random.normal(0, 0.1, 100),  # x축 가속도
    'y': np.random.normal(0, 0.1, 100),  # y축 가속도
    'z': np.random.normal(9.81, 0.1, 100)  # z축 가속도 (중력 포함)
}

# 속도 초기화
velocity = {'x': 0, 'y': 0, 'z': 0}
distance = {'x': 0, 'y': 0, 'z': 0}

# 이동 거리 계산 함수
def calculate_distance(accel, velocity, distance, dt):
    for i in range(len(accel['x'])):
        # 속도 업데이트 (적분)
        velocity['x'] += accel['x'][i] * dt
        velocity['y'] += accel['y'][i] * dt
        velocity['z'] += (accel['z'][i] - 9.81) * dt  # 중력 보정

        # 거리 업데이트 (적분)
        distance['x'] += velocity['x'] * dt
        distance['y'] += velocity['y'] * dt
        distance['z'] += velocity['z'] * dt
    
    return distance

# 이동 거리 계산
calculated_distance = calculate_distance(accel_data, velocity, distance, dt)

# 결과 출력
print("Calculated Distance (in meters):")
print(f"X: {calculated_distance['x']:.4f} meters")
print(f"Y: {calculated_distance['y']:.4f} meters")
print(f"Z: {calculated_distance['z']:.4f} meters")
