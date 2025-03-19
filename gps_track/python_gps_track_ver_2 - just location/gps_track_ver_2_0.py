#미완
import serial
import time

def read_switch_value(serial_port):
    previous_value = None

    while True:
        if serial_port.in_waiting > 0:
            # 시리얼로부터 데이터 읽기
            data = serial_port.readline().decode().strip()
            
            try:
                value = int(data)  # 읽은 값을 정수로 변환

                # 값이 변경되었을 때만 출력
                if value != previous_value:
                    print(f"Switch Value Changed: {value}")
                    previous_value = value

            except ValueError:
                # 변환에 실패하면 무시
                pass


# 시리얼 포트 설정
serial_port = 'COM6'  #본인 시리얼 통신 포트 확인하고 설정, 아두이노 포트 설정에서 확인 가능함
# 시리얼 통신 속도 설정
baud_rate = 9600

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# 수신 GPS 좌표 저장 리스트 초기화 변수 설정
coordinates = []

try:  #예외 처리 블록 시작
    while True:
        # GPS 데이터 수신
        line = ser.readline().decode('utf-8').strip()

        # GPS 데이터 파싱
        if line.startswith("Lat:"):
            try:
                # 경도와 위도 추출
                latitude = float(line.split()[1]) / 10000000.0  # 데이터 형식을 좌표식으로 맞춤.
                longitude = float(line.split()[3]) / 10000000.0
                altitude = float(line.split()[5])
                Button_siginal = float(line.split()[7])

                if(Button_siginal == 1):
                    Point_check = 0
                    Point_check += 1
                    
                    # 좌표 리스트에 추가
                    coordinates.append((latitude, longitude))  #파싱한 위도와 경도를 좌표리스트에 추가

                # 수신한 데이터 출력
                print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}, Point: {Point_check}")
            except ValueError:
                print("Invalid data format:", line)

        # 1초 대기
        time.sleep(1)

except KeyboardInterrupt:  #프로그램 종료 시 (ctrl +c) 실행되는 예외 처리 블록 시작
    print("Program terminated by user")

finally:
    ser.close()