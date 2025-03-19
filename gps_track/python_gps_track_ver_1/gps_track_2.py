import serial
import time
import folium
from flask import Flask, render_template

app = Flask(__name__)

# 시리얼 포트 설정
serial_port = 'COM6'  # 본인 시리얼 통신 포트 확인하고 설정, 아두이노 포트 설정에서 확인 가능함
# 시리얼 통신 속도 설정
baud_rate = 9600

# 수신 GPS 좌표 저장 리스트 초기화 변수 설정
coordinates = []

@app.route('/')
def index():
    return render_template('map.html', coordinates=coordinates)

def read_gps_data():
    global coordinates
    with serial.Serial(serial_port, baud_rate) as ser:
        while True:
            # GPS 데이터 수신
            line = ser.readline().decode('utf-8').strip()

            # GPS 데이터 파싱
            if line.startswith("Lat:"):
                try:
                    # 경도와 위도 추출
                    latitude = float(line.split()[1]) / 10000000.0  # 데이터 형식을 좌표식으로 맞춤.
                    longitude = float(line.split()[3]) / 10000000.0

                    # 좌표 리스트에 추가
                    coordinates.append((latitude, longitude))

                    # 수신한 데이터 출력
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
                except ValueError:
                    print("Invalid data format:", line)

                time.sleep(1)

if __name__ == '__main__':
    # GPS 데이터를 읽어오는 스레드 시작
    import threading
    gps_thread = threading.Thread(target=read_gps_data)
    gps_thread.daemon = True
    gps_thread.start()

    # Flask 애플리케이션 실행
    app.run(debug=True)
