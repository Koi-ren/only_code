import pandas as pd
import numpy as np

# 엑셀 파일에서 데이터 읽어오기
planing_data = pd.read_excel('path_planning_data.xlsx')
planning_point_data, lat_data, lon_data = planing_data['point number'], planing_data['latitude'], planing_data['longitude']

# 사용자가 입력한 좌표 값
lat_input_value = float(input("위도 값을 입력하세요: "))
lon_input_value = float(input("경도 값을 입력하세요: "))

# 위도, 경도 중 입력한 값에 가장 가까운 값 찾기
lat_closest_value = min(lat_data, key=lambda x: abs(x - lat_input_value))
lon_closest_value = min(lon_data, key=lambda x: abs(x - lon_input_value))

# 가장 근사한 값에 해당하는 인덱스 찾기
lat_index = lat_data[lat_data == lat_closest_value].index[0]
lon_index = lon_data[lon_data == lon_closest_value].index[0]

# 근사값이 같을 경우 출력, 다를 경우 경고
if lat_index == lon_index:
    point_number = planning_point_data[lat_index]
    print(f"가장 근사한 좌표는:\n포인트 넘버: {point_number}, 위도: {lat_closest_value}, 경도: {lon_closest_value}")
else:
    index = (lat_index + lon_index)/2
    if index in planning_point_data.values:
        point_index = planning_point_data[planning_point_data == index].index[0]
        
        lat_value = lat_data[point_index]
        lon_value = lon_data[point_index]


    print("입력한 위도와 경도 값이 서로 다른 포인트에 근사합니다. 다시 입력해주세요.")
