import openpyxl
import os

def decimal_to_dms(decimal):
    degrees = int(decimal)
    minutes_full = abs(decimal - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60
    return degrees, minutes, seconds

def create_excel_with_dms(latitude, longitude, filename='coordinates.xlsx'):
    # DMS 변환
    lat_deg, lat_min, lat_sec = decimal_to_dms(latitude)
    lon_deg, lon_min, lon_sec = decimal_to_dms(longitude)

    lat_direction = "N" if lat_deg >= 0 else "S"
    lon_direction = "E" if lon_deg >= 0 else "W"
    
    lat_deg = abs(lat_deg)
    lon_deg = abs(lon_deg)
    
    # 엑셀 파일 생성
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Coordinates"

    # 헤더 추가
    sheet.append(["Latitude", "Direction", "Longitude", "Direction"])

    # 도분초 값을 엑셀에 추가
    sheet.append([
        f"{lat_deg}°{lat_min}'{lat_sec:.2f}\"", lat_direction,
        f"{lon_deg}°{lon_min}'{lon_sec:.2f}\"", lon_direction
    ])

    # 엑셀 파일 저장
    workbook.save(filename)
    print(f"엑셀 파일이 '{os.path.abspath(filename)}'에 생성되었습니다.")

# 예시 좌표
latitude = 37.7749
longitude = -122.4194

# 엑셀 파일 생성 경로 지정
save_path = "C:/Users/plane/Desktop/park_ws/gps_track/way_point_coordinates.xlsx"
create_excel_with_dms(latitude, longitude, filename=save_path)