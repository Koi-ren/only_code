#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import time

# 아두이노와의 시리얼 통신 설정
ser_motor = serial.Serial('/dev/ttyMOTORspeed', 115200, timeout=1)  # 구동 모터용 시리얼
ser_steering = serial.Serial('/dev/ttysteering', 115200, timeout=1)  # 조향 모터용 시리얼
time.sleep(2)  # 시리얼 통신 초기화 대기

# 파이썬 코드 내에서 모터 속도 및 조향 각도를 지정
speed = 50 # 전방 및 후방 바퀴 속도 (0-255)
steering_angle = 0  # 조향 각도 (-45 ~ 43)

def send_motor_speed(speed):
    """ 구동 모터 속도 값을 아두이노로 전송 """
    data = f"{speed}\n"
    ser_motor.write(data.encode())
    print(f"Sent Motor Speed: {speed}")

def send_steering_angle(angle):
    """ 조향 각도 값을 아두이노로 전송 """
    data = f"{angle}\n"
    ser_steering.write(data.encode())
    print(f"Sent Steering Angle: {angle}")

def stop_motors():
    """ 모터를 정지시키기 위해 속도 0을 아두이노로 전송 """
    send_motor_speed(0)  # 모터를 완전히 멈추기 위해 0 전송
    print("Motors stopped.")

def stop_steering():
    """ 조향을 중앙으로 맞추기 위해 각도 0을 아두이노로 전송 """
    send_steering_angle(0)  # 조향을 0도로 맞추기 위해 0 전송
    print("Steering centered.")

def main():
    try:
        while True:
            # 모터 속도와 조향 각도 아두이노로 지속적으로 전송
            send_motor_speed(speed)  # 구동 모터 속도 전송
            send_steering_angle(steering_angle)  # 조향 각도 전송
            time.sleep(1)  # 1초마다 속도 및 각도 업데이트
    except KeyboardInterrupt:
        # 프로그램 종료 시 모터와 조향을 멈춤
        print("\nStopping motors and steering...")
        stop_motors()  # 모터 멈춤
        time.sleep(0.1)  # 잠시 대기하여 멈춘 상태 확실히 반영
        stop_steering()  # 조향 멈춤
        time.sleep(0.1)  # 잠시 대기하여 멈춘 상태 확실히 반영
    finally:
        # 시리얼 포트 닫기
        if ser_motor.is_open:
            ser_motor.close()
            print("Motor serial port closed.")
        if ser_steering.is_open:
            ser_steering.close()
            print("Steering serial port closed.")

if __name__ == "__main__":
    main()

