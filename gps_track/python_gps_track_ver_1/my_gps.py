from flask import Flask, render_template
import serial
import time


app = Flask(__name__)

# 시리얼 포트 설정
serial_port = 'COM6'  # 본인 시리얼 통신 포트 확인하고 설정, 아두이노 포트 설정에서 확인 가능함
# 시리얼 통신 속도 설정
baud_rate = 9600

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# 초기 위치 설정
latitude = 0
longitude = 0

@app.route('/')
def index():
    return render_template('map2.html', latitude=latitude, longitude=longitude)

def read_gps_data():
    global latitude, longitude
    while True:
        # GPS 데이터 수신
        line = ser.readline().decode('utf-8').strip()

        # GPS 데이터 파싱
        if line.startswith("Lat:"):
            try:
                # 경도와 위도 추출
                latitude = float(line.split()[1]) / 10000000.0  # 데이터 형식을 좌표식으로 맞춤.
                longitude = float(line.split()[3]) / 10000000.0

                print(f"Latitude: {latitude}, Longitude: {longitude}")

            except ValueError:
                print("Invalid data format:", line)

        # 잠시 대기
        time.sleep(1)

if __name__ == '__main__':
    # GPS 데이터를 읽어오는 스레드 시작
    import threading
    gps_thread = threading.Thread(target=read_gps_data)
    gps_thread.daemon = True
    gps_thread.start()

    # Flask 애플리케이션 실행
    app.run(debug=True)
