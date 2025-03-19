import serial
import time
import webbrowser
from folium import Map, Marker, PolyLine
import folium

# 라이브러리 버전 확인
print(f"folium version: {folium.__version__}")
# 시리얼 포트 설정
serial_port = 'COM6'  # 본인 시리얼 통신 포트 확인하고 설정, 아두이노 포트 설정에서 확인 가능함
baud_rate = 9600

# 지도 중심 좌표 설정 (예시: 서울)
center_latitude = 37.566535
center_longitude = 126.977942

# 지도 줌 레벨 설정
zoom_start = 15

# 이동 방향 화살표 마커 이미지 설정
arrow_head_image = 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png'

# 폴리라인 색상 설정
polyline_color = '#0000FF'  # 파란색

# 좌표 저장 리스트 초기화
coordinates = []
def update_map(polyline):
    global coordinates, map, marker

    # 최근 좌표 추출
    try:
        latitude = coordinates[-1][0]
        longitude = coordinates[-1][1]
    except IndexError:
        return

    # 지도 중심 업데이트
    map.location = [latitude, longitude]

    # 마커 위치 업데이트
    marker.location = [latitude, longitude]

    # 폴리라인 업데이트
    polyline.add_child(Marker(location=[latitude, longitude]))

    # 지도 레이어 다시 그리기
    map.render()

    # 웹 브라우저 새로고침
    webbrowser.open(map._repr_html_(), new=0, autoraise=True)

def main():
    global coordinates, map, marker

    # 시리얼 포트 열기
    ser = serial.Serial(serial_port, baud_rate)

    # 지도 생성
    map = Map(location=[center_latitude, center_longitude], zoom_start=zoom_start)

    # 이동 방향 화살표 마커 생성
    marker = Marker(location=[center_latitude, center_longitude],
                    icon=folium.Icon(icon=arrow_head_image, icon_size=(20, 30)))

    # 폴리라인 생성
    polyline = PolyLine(locations=[[center_latitude, center_longitude]], color=polyline_color)

    # 지도 레이어 추가
    map.add_child(marker)
    map.add_child(polyline)

    # 웹 브라우저 열기
    webbrowser.open_new_tab(map._repr_html_())

    try:
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
                    coordinates.append((latitude, longitude))  # 파싱한 위도와 경도를 좌표리스트에 추가

                    # 2초 간격으로 지도 업데이트
                    if len(coordinates) % 2 == 0:
                        update_map(polyline)

                except ValueError:
                    print("Invalid data format:", line)

            # 1초 대기
            time.sleep(1)

    except KeyboardInterrupt:
        print("프로그램 종료")
        ser.close()

    except Exception as e:
        print(f"오류 발생: {e}")
        ser.close()

if __name__ == "__main__":
    main()