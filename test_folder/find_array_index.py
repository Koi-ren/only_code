import pandas as pd

# 예시 데이터
lat_data = pd.Series([12.34, 45.74, 89.01, 23.45, 45.67])

# 찾고자 하는 값
lat_closest_value = 45.67

# lat_closest_value와 일치하는 값의 첫 번째 인덱스 찾기
lat_index = lat_data[lat_data == lat_closest_value].index[0]

print(f"Closest value {lat_closest_value} is at index {lat_index}")
