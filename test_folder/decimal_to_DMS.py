def decimal_to_dms(decimal):
    # 도(degree) 구하기
    degrees = int(decimal)

    # 분(minutes) 구하기
    minutes_full = abs(decimal - degrees) * 60
    minutes = int(minutes_full)

    # 초(seconds) 구하기
    seconds = (minutes_full - minutes) * 60

    return degrees, minutes, seconds

# 예시 좌표값 (위도 및 경도)
latitude = 37.7749
longitude = -122.4194

# 위도 변환
lat_deg, lat_min, lat_sec = decimal_to_dms(latitude)
lat_direction = "N" if lat_deg >= 0 else "S"
lat_deg = abs(lat_deg)

# 경도 변환
lon_deg, lon_min, lon_sec = decimal_to_dms(longitude)
lon_direction = "E" if lon_deg >= 0 else "W"
lon_deg = abs(lon_deg)

# 결과 출력
print(f"위도: {lat_deg}°{lat_min}'{lat_sec:.2f}\" {lat_direction}")
print(f"경도: {lon_deg}°{lon_min}'{lon_sec:.2f}\" {lon_direction}")
