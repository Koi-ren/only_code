import numpy as np
import openpyxl

#k+1
point_number = 29 

raw_save_path = "C:/Users/plane/Desktop/park_ws/gps_track/devide_point_28m_re.xlsx"

def save_to_excel(sheet, point_index, latitude, longitude):
    sheet.append([point_index, f"{latitude}", f"{longitude}"])

# x축과 y축의 시작 값과 끝 값
x1, y1 = 35.120089996748, 129.102152825105
x2, y2 = 35.11988115056941,  129.102843350201

# k등분한 x축 값과 y축 값 구하기 (총 k+1개의 점을 포함)
x_values = np.linspace(x1, x2, point_number)
y_values = np.linspace(y1, y2, point_number)

# 새로운 워크북 생성
raw_workbook = openpyxl.Workbook()
raw_sheet = raw_workbook.active
raw_sheet.title = "devide_point"
raw_sheet.append(["Point Number", "Latitude", "Longitude"])

# x축과 y축의 결과 좌표 및 순서 번호 출력 및 저장
for idx, (x, y) in enumerate(zip(x_values, y_values), start=1):
    save_to_excel(raw_sheet, idx, x, y)
    print(f"{idx}: ({x:.15f}, {y:.15f})")

# 엑셀 파일로 저장
raw_workbook.save(raw_save_path)
