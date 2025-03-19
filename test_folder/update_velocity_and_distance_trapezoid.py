import numpy as np

# 샘플링 시간 간격 (초)
dt = 0.01  # 100Hz 샘플링

# 속도 및 거리 초기화
velocity = {0:0, 1:0, 2:0}
distance = {0:0, 1:0, 2:0}
prev_accel = [0, 0, 0]  # 이전 가속도 초기화

def update_velocity_and_distance_trapezoid(accel, prev_accel, velocity, distance, dt):
    """
    트라페zoid 적분법을 사용하여 속도와 이동 거리를 업데이트하는 함수
    :param accel: 현재 가속도 샘플 (x, y, z)
    :param prev_accel: 이전 가속도 샘플 (x, y, z)
    :param velocity: 현재 속도 (딕셔너리 형태)
    :param distance: 현재 이동 거리 (딕셔너리 형태)
    :param dt: 샘플링 시간 간격
    """
    # 트라페zoid 적분법으로 속도 업데이트
    velocity[0] += ((accel[0] + prev_accel[0]) / 2) * dt
    velocity[1] += ((accel[1] + prev_accel[1]) / 2) * dt
    velocity[2] += ((accel[2] + prev_accel[2] - 9.81 * 2) / 2) * dt  # 중력 보정 포함

    # 거리 업데이트 (적분)
    distance[0] += velocity[0] * dt
    distance[1] += velocity[1] * dt
    distance[2] += velocity[2] * dt

    return velocity, distance

# 예시 가속도 데이터
acceleration_sample = [0.013411321677267551, -0.007121371570974588, -1.0206421613693237]

# 트라페zoid 적분법을 이용해 속도 및 거리 업데이트
velocity, distance = update_velocity_and_distance_trapezoid(acceleration_sample, prev_accel, velocity, distance, dt)

# 업데이트된 가속도를 이전 가속도로 저장
prev_accel = acceleration_sample

# 결과 출력
print("Updated Velocity (m/s):")
print(f"X: {velocity[1 ]:.4f}")
print(f"Y: {velocity[2 ]:.4f}")
print(f"Z: {velocity['z']:.4f}")

print("Updated Distance (meters):")
print(f"X: {distance[1 ]:.4f}")
print(f"Y: {distance[2 ]:.4f}")
print(f"Z: {distance['z']:.4f}")
