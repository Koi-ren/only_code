import serial
import time

#시리얼 포트 설정
serial_port = 'COM12'
#시리얼 통신 속도 설정
baud_rate = 9600

#시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)
try:  #예외 처리 블록 시작
    while True:
        #스로틀 신호 수신
        measurement = ser.readline().decode('utf-8').strip()

        if measurement.startswith(" Throttle_value: "):
            try:
                #스로틀 신호와 정제된 신호(low-pass-filter) 추출
                #스로틀 신호: measurement.split()[1]
                #정제된 신호: measurement.split()[3]
                Throttle_value = int(measurement.split()[1])
                filtered_value = int(measurement.split()[3])

                #수신한 데이터 출력
                print(f'Throttle_value: {Throttle_value}, Filtered_value: {filtered_value}')

            #왜곡된 신호 입력될 시 오류 출력문
            except ValueError:
                print("Invalid data format:", measurement)

        # 1초 대기
        time.sleep(1)

#프로그램 종료 시 (ctrl +c) 실행되는 예외 처리 블록 시작
except KeyboardInterrupt:  
    print("Program terminated by user")

#최종 처리
finally:
    # 시리얼 포트 닫기
    ser.close()