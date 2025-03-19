from rplidar import RPLidar

# RPLidar 포트 설정
PORT_NAME = 'COM7'  # RPLidar가 연결된 포트명

# 임계값 설정
THRESHOLD_DISTANCE = 1200  # 거리 임계값 (mm)

# RPLidar 초기화
lidar = RPLidar(PORT_NAME)

try:
    print("Scanning...")
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            if distance < THRESHOLD_DISTANCE:
                # 거리와 각도를 화면에 출력
                print(f"Object detected at angle {angle} with distance {distance} mm")
except KeyboardInterrupt:
    print("Stopped by user")

# RPLidar 정지 및 연결 해제
lidar.stop()
lidar.disconnect()
