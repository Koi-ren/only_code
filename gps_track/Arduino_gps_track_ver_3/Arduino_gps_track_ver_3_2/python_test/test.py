import serial
import threading

# 아두이노 장치 A와 B의 COM 포트와 보드레이트 설정
com_port_a = 'COM6'   # 코드 A가 연결된 포트
com_port_b = 'COM26'  # 코드 B가 연결된 포트
baud_rate = 9600      # 아두이노와 동일한 보드레이트 설정

# 시리얼 포트 초기화
serial_a = serial.Serial(com_port_a, baud_rate, timeout=1)
serial_b = serial.Serial(com_port_b, baud_rate, timeout=1)

# 로그 데이터를 수신하고 출력하는 함수
def read_serial_data(serial_port, label):
    while True:
        if serial_port.in_waiting > 0:
            data = serial_port.readline().decode('utf-8').strip()
            if data:
                print(f"{label}: {data}")

# 스레드를 사용해 두 포트에서 동시에 데이터 수신
thread_a = threading.Thread(target=read_serial_data, args=(serial_a, "Arduino A"))
thread_b = threading.Thread(target=read_serial_data, args=(serial_b, "Arduino B"))

# 스레드 시작
thread_a.start()
thread_b.start()

# 메인 스레드는 종료되지 않도록 대기
thread_a.join()
thread_b.join()
