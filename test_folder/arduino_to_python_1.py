import serial

# 시리얼 포트와 보드레이트 설정
ser = serial.Serial('COM30', 115200)  # COM 포트는 상황에 맞게 변경

def parse_gnss_data(data):
    lines = data.splitlines()
    gnss_1 = {}
    gnss_2 = {}

    for i, line in enumerate(lines):
        if line.startswith("GNSS_1:"):
            # 각 라인에서 ":" 이후 값을 가져오고, 공백이나 잘못된 데이터를 처리
            try:
                gnss_1['Lat'] = float(lines[i+1].split(': ')[1].strip())
                gnss_1['Long'] = float(lines[i+2].split(': ')[1].strip())
                gnss_1['Alt'] = float(lines[i+3].split(': ')[1].strip())
            except (IndexError, ValueError) as e:
                print(f"Error parsing GNSS_1 data: {e}")
        elif line.startswith("GNSS_2:"):
            try:
                gnss_2['Lat'] = float(lines[i+1].split(': ')[1].strip())
                gnss_2['Long'] = float(lines[i+2].split(': ')[1].strip())
                gnss_2['Alt'] = float(lines[i+3].split(': ')[1].strip())
            except (IndexError, ValueError) as e:
                print(f"Error parsing GNSS_2 data: {e}")

    return gnss_1, gnss_2

while True:
    if ser.in_waiting > 0:
        line = ser.read_until().decode('utf-8')
        if "GNSS_1:" in line or "GNSS_2:" in line:
            data = ser.read(100).decode('utf-8')  # 데이터 크기에 맞게 조정
            gnss_1, gnss_2 = parse_gnss_data(data)
            print(f"GNSS 1: {gnss_1}")
            print(f"GNSS 2: {gnss_2}")
