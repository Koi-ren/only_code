import pandas as pd

# 엑셀 파일 불러오기
file_path = 'C:/Users/plane/Desktop/park_ws/gps+imu_drive/imu_distance_3.xlsx'
df = pd.read_excel(file_path)

# 필요한 열 이름 변경
df.columns = ['time', 'x_axis', 'y_axis']

import matplotlib.pyplot as plt

# 시각화: x, y, z 값을 시간에 따라 플롯
plt.figure(figsize=(10, 6))

# x축 데이터 시각화
plt.plot(df['time'], df['x_axis'], label='X Axis', color='r')
# y축 데이터 시각화
plt.plot(df['time'], df['y_axis'], label='Y Axis', color='g')
# z축 데이터 시각화

# 그래프 세부 설정
plt.title('stemp vs X, Y')
plt.xlabel('stemp/300 = time(s)')
plt.ylabel('Axis Values (m)')
plt.legend()
plt.grid(True)

# 그래프 보여주기
plt.show()
