import pandas as pd
import numpy as np

def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate the bearing from (lat1, lon1) to (lat2, lon2)."""
    delta_lon = lon2 - lon1
    x = np.sin(np.deg2rad(delta_lon)) * np.cos(np.deg2rad(lat2))
    y = np.cos(np.deg2rad(lat1)) * np.sin(np.deg2rad(lat2)) - np.sin(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.cos(np.deg2rad(delta_lon))
    initial_bearing = np.arctan2(x, y)
    initial_bearing = np.rad2deg(initial_bearing)
    bearing = (initial_bearing + 360) % 360
    return bearing

# 엑셀 파일에서 데이터 읽어오기
df = pd.read_excel('C:/Users/plane/Desktop/park_ws/test_folder/tu_lat_lon.xlsx')

# 데이터프레임 열 이름 확인
print(df.columns)

# x축과 y축 시작 및 끝 좌표 가져오기
point_number = df['point_number']
lat_start = df['lat']
lon_start = df['lon']

# 다음 포인트 좌표를 추가하기 위해 데이터프레임 생성
df['next_lat'] = df['lat'].shift(-1)
df['next_lon'] = df['lon'].shift(-1)

# 각 포인트의 방향 계산
bearings = []
for i in range(len(df) - 1):
    lat1, lon1 = df.loc[i, 'lat'], df.loc[i, 'lon']
    lat2, lon2 = df.loc[i + 1, 'next_lat'], df.loc[i + 1, 'next_lon']
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    bearings.append(bearing)

# 마지막 포인트는 방향이 없으므로 NaN 추가
bearings.append(np.nan)

df['bearing'] = bearings

# 엑셀 파일로 저장하기
df.to_excel('C:/Users/plane/Desktop/park_ws/test_folder/updated_file.xlsx', index=False)

print("Updated Excel file with bearings saved as 'updated_file.xlsx'.")
