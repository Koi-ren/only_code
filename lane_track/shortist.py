import serial
import time
import matplotlib.pyplot as plt
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point


# 시리얼 통신 설정
ser = serial.Serial('COM6', 9600)  # 포트 번호는 사용하는 환경에 따라 다를 수 있음

# 초기화를 위한 더미 데이터
prev_longitude, prev_latitude = 0, 0

# OSMnx를 사용하여 도로 네트워크 가져오기
G = ox.graph_from_place('Seoul, South Korea', network_type='all')

# 지도 위에 좌표를 표시하기 위한 GeoDataFrame 생성
gdf = gpd.GeoDataFrame(geometry=[Point(0, 0)], crs="EPSG:4326")

# 지도 설정
fig, ax = ox.plot_graph(ox.project_graph(G), show=False, close=False)
ax.set_xlim(126, 130)  # 경도 범위 수정
ax.set_ylim(34, 38)    # 위도 범위 수정
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Bluetooth GPS Data')

try:
    while True:
        # 아두이노에서 데이터 읽기
        data = ser.readline().decode('utf-8').strip()

        try:
            # 데이터 파싱
            parts = data.split()
            if len(parts) >= 5:
                # 기대하는 최소 개수의 값이 있는 경우에만 처리
                for part in parts:
                    if part.startswith("Lat:"):
                        latitude = float(part.split(":")[1])
                    elif part.startswith("Long:"):
                        longitude = float(part.split(":")[1])
                    elif part.startswith("Alt:"):
                        altitude = int(part.split(":")[1])
                    elif part.startswith("SIV:"):
                        siv = int(part.split(":")[1])

                # GeoDataFrame에 새로운 좌표 추가
                gdf = gdf.append({'geometry': Point(longitude, latitude)}, ignore_index=True)

                # GeoDataFrame을 지도 위에 표시
                gdf.plot(ax=ax, color='red', markersize=50, alpha=0.5)

                # 이전 좌표 기록
                prev_longitude, prev_latitude = longitude, latitude

                # 그래프 업데이트
                plt.pause(1)  # 1초에 한 번 업데이트

        except ValueError as e:
            print(e)
            continue

except KeyboardInterrupt:
    # 프로그램 종료 시 시리얼 포트 닫기
    ser.close()

plt.show()
