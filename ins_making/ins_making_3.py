import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 시리얼 포트와 속도를 설정합니다.
ser = serial.Serial('COM13', 9600)  # 아두이노가 연결된 포트를 사용하세요 (예: 'COM3' 또는 '/dev/ttyUSB0')

# EKF 초기 설정
dt = 0.01  # 시간 간격 (100ms)
Q = np.eye(3) * 0.01  # 프로세스 노이즈 공분산 행렬
R = np.eye(2) * 1000  # 측정 노이즈 공분산 행렬 (Yaw는 자이로스코프만 사용하므로 측정값 없음)
P = np.eye(3)  # 오차 공분산 행렬
x = np.zeros((3, 1))  # 상태 벡터 (roll, pitch, yaw)

def ekf_predict(x, P, gyro, dt):
    # 상태 예측
    F = np.eye(3)
    F[0, 1] = -dt
    F[1, 0] = dt
    x = x + gyro.reshape((3, 1)) * dt

    # 오차 공분산 예측
    P = np.dot(F, np.dot(P, F.T)) + Q

    return x, P

def ekf_update(x, P, accel):
    # 가속도계로부터 측정
    roll_meas = np.arctan2(accel[1], accel[2])
    pitch_meas = np.arctan2(-accel[0], np.sqrt(accel[1]**2 + accel[2]**2))
    z = np.array([[roll_meas], [pitch_meas]])

    # 칼만 이득 계산
    H = np.zeros((2, 3))
    H[0, 0] = 1
    H[1, 1] = 1
    y = z - np.dot(H, x)
    S = np.dot(H, np.dot(P, H.T)) + R
    K = np.dot(P, np.dot(H.T, np.linalg.inv(S)))

    # 상태 업데이트
    x = x + np.dot(K, y)

    # 오차 공분산 업데이트
    P = P - np.dot(K, np.dot(H, P))

    return x, P

# 그래프 설정
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
ax1.set_title("Roll")
ax2.set_title("Pitch")
ax3.set_title("Yaw")

x_len = 100  # X축 길이 (시간)
y_range = (-np.pi, np.pi)  # Y축 범위 (각도)

roll_data, pitch_data, yaw_data = [0]*x_len, [0]*x_len, [0]*x_len

ax1.set_ylim(y_range)
ax2.set_ylim(y_range)
ax3.set_ylim(y_range)

line_roll, = ax1.plot(roll_data, label='Roll')
line_pitch, = ax2.plot(pitch_data, label='Pitch')
line_yaw, = ax3.plot(yaw_data, label='Yaw')

ax1.legend()
ax2.legend()
ax3.legend()

def update_data(frame):
    global x, P
    # 시리얼 데이터를 읽고 파싱
    line = ser.readline().decode('utf-8').strip()
    try:
        ax, ay, az, gx, gy, gz = map(int, line.split(','))
    except ValueError:
        return line_roll, line_pitch, line_yaw

    # 가속도계 및 자이로스코프 데이터를 처리
    accel = np.array([ax, ay, az])
    gyro = np.array([gx, gy, gz]) / 131.0  # 자이로스코프 데이터를 각속도로 변환

    # EKF 예측 단계
    x, P = ekf_predict(x, P, gyro, dt)

    # EKF 업데이트 단계
    x, P = ekf_update(x, P, accel)

    # Roll, Pitch 및 Yaw 데이터를 업데이트
    roll_data.append(x[0, 0])
    pitch_data.append(x[1, 0])
    yaw_data.append(x[2, 0])

    roll_data.pop(0)
    pitch_data.pop(0)
    yaw_data.pop(0)

    # 그래프 업데이트
    line_roll.set_ydata(roll_data)
    line_pitch.set_ydata(pitch_data)
    line_yaw.set_ydata(yaw_data)

    return line_roll, line_pitch, line_yaw

# 애니메이션 실행
ani = animation.FuncAnimation(fig, update_data, blit=True, interval=100)

plt.show()

# 시리얼 포트를 닫습니다.
ser.close()
