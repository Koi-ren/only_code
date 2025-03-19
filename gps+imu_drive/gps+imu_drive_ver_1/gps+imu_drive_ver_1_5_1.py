import openpyxl
import folium

# 엑셀 파일 경로 설정
gps_imu_coordinates_save_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/gps+imu_coordinates.xlsx"

# Folium 맵 생성
def create_map(center_lat, center_lon):
    return folium.Map(location=[center_lat, center_lon], zoom_start=15)

# 좌표를 지도에 표시하는 함수
def plot_coordinates(sheet, color, tooltip, map_obj):
    for row in sheet.iter_rows(min_row=2, values_only=True):
        point_number, latitude, longitude = row

        # 좌표값이 None이거나 유효하지 않은 경우 무시
        if latitude is None or longitude is None:
            continue

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            continue  # 좌표값이 숫자가 아닌 경우 무시

        folium.CircleMarker(
            location=[latitude, longitude],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.8,
            tooltip=f"{tooltip}: Point {point_number}\nLat: {latitude}, Lon: {longitude}"
        ).add_to(map_obj)

# 엑셀 파일 열기
gps_imu_coordinates_workbook = openpyxl.load_workbook(gps_imu_coordinates_save_path)
gps_imu_coordinates_sheet = gps_imu_coordinates_workbook.active

# 맵 초기화 (중심점을 첫 번째 좌표로 설정)
initial_latitude = 35.1204103  # 초기 위치 설정
initial_longitude = 129.100915

mymap = create_map(initial_latitude, initial_longitude)

# 원본 좌표 (초록색)
plot_coordinates(gps_imu_coordinates_sheet, "green", "Raw Data", mymap)

# 지도를 HTML 파일로 저장
output_html_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/gps+imu_map.html"
mymap.save(output_html_path)

print(f"Folium 지도가 '{output_html_path}'에 저장되었습니다.")
