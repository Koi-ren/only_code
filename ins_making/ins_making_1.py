import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 시리얼 포트와 속도를 설정합니다.
ser = serial.Serial('COM13', 9600)  # 아두이노가 연결된 포트를 사용하세요 (예: 'COM3' 또는 '/dev/ttyUSB0')

# 그래프 설정
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_title("Accelerometer")
ax2.set_title("Gyroscope")

x_len = 100  # X축 길이 (시간)
y_range = (-50000, 50000)  # Y축 범위 (센서 데이터 범위)

# 가속도계와 자이로스코프 데이터 저장 공간
ax_data, ay_data, az_data = [0]*x_len, [0]*x_len, [0]*x_len
gx_data, gy_data, gz_data = [0]*x_len, [0]*x_len, [0]*x_len

# 그래프 초기 설정
ax1.set_ylim(y_range)
ax2.set_ylim(y_range)

line_ax, = ax1.plot(ax_data, label='Ax')
line_ay, = ax1.plot(ay_data, label='Ay')
line_az, = ax1.plot(az_data, label='Az')

line_gx, = ax2.plot(gx_data, label='Gx')
line_gy, = ax2.plot(gy_data, label='Gy')
line_gz, = ax2.plot(gz_data, label='Gz')

ax1.legend()
ax2.legend()

# 애니메이션 함수
def update_data(frame):
    # 시리얼 데이터를 읽고 파싱
    line = ser.readline().decode('utf-8').strip()
    try:
        ax, ay, az, gx, gy, gz = map(int, line.split(','))
    except ValueError:
        return line_ax, line_ay, line_az, line_gx, line_gy, line_gz

    # 최신 데이터를 리스트에 추가하고, 오래된 데이터를 제거
    ax_data.append(ax)
    ay_data.append(ay)
    az_data.append(az)
    gx_data.append(gx)
    gy_data.append(gy)
    gz_data.append(gz)

    ax_data.pop(0)
    ay_data.pop(0)
    az_data.pop(0)
    gx_data.pop(0)
    gy_data.pop(0)
    gz_data.pop(0)

    # 그래프 업데이트
    line_ax.set_ydata(ax_data)
    line_ay.set_ydata(ay_data)
    line_az.set_ydata(az_data)
    line_gx.set_ydata(gx_data)
    line_gy.set_ydata(gy_data)
    line_gz.set_ydata(gz_data)

    return line_ax, line_ay, line_az, line_gx, line_gy, line_gz

# 애니메이션 실행
ani = animation.FuncAnimation(fig, update_data, blit=True, interval=100)

plt.show()

# 시리얼 포트를 닫습니다.
ser.close()
