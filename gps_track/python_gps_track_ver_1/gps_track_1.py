import serial
import time
import folium

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

                # 좌표 리스트에 추가
                coordinates.append((latitude, longitude))  #파싱한 위도와 경도를 좌표리스트에 추가

                # 수신한 데이터 출력
                print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")
            except ValueError:
                print("Invalid data format:", line)

        # 1초 대기
        time.sleep(1)

except KeyboardInterrupt:  #프로그램 종료 시 (ctrl +c) 실행되는 예외 처리 블록 시작
    print("Program terminated by user")

finally:  #최종 처리 블록 시작
    # 시리얼 포트 닫기
    ser.close()

    # Google 지도에 GPS 데이터 표시
    if coordinates:
        # 처음 받은 좌표를 중심으로 하는 지도 생성
        m = folium.Map(location=coordinates[0], zoom_start=15)

        # 모든 좌표를 연결하는 선 그리기
        folium.PolyLine(locations=coordinates, color='blue').add_to(m)

        # 지도를 HTML 파일로 저장
        save_path = r'C:\Users\plane\Desktop\park_ws\gps_track\map.html'
        m.save(save_path)
        print(f"Map saved to: {save_path}")   #저장 경로 출력
    else:
        print("No GPS data received.")  #GPS 데이터가 수신되지 않을 떄 출력
