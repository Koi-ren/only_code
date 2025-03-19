#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import time
import signal
import sys
from multiprocessing import Pipe, Process
from plt_cam import plt_cam  # plt_motor.py 파일에서 함수 임포트
import rospy
from std_msgs.msg import Float32

# 시리얼 통신 설정 (조향 모터 및 구동 모터)
arduino_steering = serial.Serial('/dev/ttysteering', 115200, timeout=1)  # 조향 모터용 시리얼 포트
arduino_drive = serial.Serial('/dev/ttyMOTORspeed', 115200, timeout=1)  # 구동 모터용 시리얼 포트
time.sleep(2)  # 시리얼 초기화 대기

# 모터 및 조향각 전송 주기 설정
speed = 30  # 기본 구동 모터 속도 (0-255 범위)
steering_send_interval = 0.05  # 조향각 전송 주기
speed_send_interval = 1  # 모터 속도 전송 주기

ros_speed = None
ros_angle = None

w1 = 0.6
w2 = 0.4

# 타이머 설정
last_steering_sent_time = time.time()
last_speed_sent_time = time.time()

# 프로그램 종료 플래그
running = True
stop_received = False  # 'stop' 메시지 수신 여부를 확인하는 플래그

def speed_callback(data):
    global speed
    speed = data.data
    rospy.loginfo(f"Received speed data: {speed}")

def angle_callback(data):
    global angle
    angle = data.data
    rospy.loginfo(f"Received angle data: {angle}")

# 조향각을 아두이노로 전송하는 함수
def send_steering_angle(angle):
    global last_steering_sent_time
    current_time = time.time()
    if current_time - last_steering_sent_time > steering_send_interval:
        data = f"{angle}\n"
        arduino_steering.write(data.encode())
        print(f"Sent Steering Angle: {angle}")  # 디버깅용 출력
        last_steering_sent_time = current_time

# 모터 속도를 아두이노로 전송하는 함수
def send_motor_speed(speed):
    global last_speed_sent_time
    current_time = time.time()
    if current_time - last_speed_sent_time > speed_send_interval:
        data = f"{speed}\n"
        arduino_drive.write(data.encode())
        print(f"Sent Motor Speed: {speed}")
        last_speed_sent_time = current_time

# 모터 및 조향을 정지시키는 함수
def stop_motors_and_steering():
    """ 모터와 조향을 정지시킴 """
    if arduino_drive.is_open:
        send_motor_speed(0)  # 모터 속도를 0으로 설정
        time.sleep(0.1)  # 전송 후 잠깐 대기
        arduino_drive.flush()  # 버퍼 비우기
        print("Motors stopped.")
    if arduino_steering.is_open:
        send_steering_angle(0)  # 조향 각도를 0도로 설정
        time.sleep(0.1)  # 전송 후 잠깐 대기
        arduino_steering.flush()  # 버퍼 비우기
        print("Steering centered.")

# 프로그램 종료 시 호출되는 핸들러
def signal_handler(sig, frame):
    global running
    print("프로그램을 종료합니다.")
    
    # 모터와 조향 정지
    stop_motors_and_steering()

    # 시리얼 포트 닫기
    if arduino_drive.is_open:
        arduino_drive.flush()  # 전송 대기
        arduino_drive.close()
        print("Motor serial port closed.")
    	
    if arduino_steering.is_open:
        arduino_steering.flush()  # 전송 대기
        arduino_steering.close()
        print("Steering serial port closed.")
        
    # 프로그램 종료
    sys.exit(0)

# Ctrl+C (SIGINT) 신호 처리 등록
signal.signal(signal.SIGINT, signal_handler)

# 파이프를 통해 조향각을 받아 처리하는 메인 함수
def receive_steering_angle(pipe):
    global speed, stop_received, ros_angle  # speed 값과 stop_received 플래그를 제어하기 위해 global로 설정

    while running:
        try:
            # 파이프에서 조향각 또는 stop 신호 수신
            if pipe.poll():
                message, steering_angle = pipe.recv()

                # 'stop' 메시지를 받으면 모터 속도를 0으로 설정하고 플래그 활성화
                if message == "stop":
                    print("Received 'stop' signal. Stopping motors.")
                    send_motor_speed(0)  # 모터 속도 0 설정
                    stop_received = True  # stop 신호 수신 플래그 설정

                elif ros_speed == 0.0:
                    print("stop")
                    send_motor_speed(0)
                    stop_received = True
                else:
                    # stop 메시지를 받은 후에는 조향각과 속도를 전송하지 않음
                    if not stop_received:
                        
                        real_steering_angle = w1*steering_angle + w2*ros_angle
                        send_steering_angle(real_steering_angle)
                        send_motor_speed(speed)
        except Exception as e:
            print(f"Error while receiving data from pipe: {e}")
            break

if __name__ == "__main__":
    # 파이프 생성
    parent_pipe, child_pipe = Pipe()
    rospy.init_node('sensor_subscriber')
    
    # 자식 프로세스 시작 (plt_motor 함수 실행)
    p = Process(target=plt_cam, args=(child_pipe,))
    p.start()

    try:
        rospy.Subscriber('speed_topic', Float32, speed_callback)
        rospy.Subscriber('angle_topic', Float32, angle_callback)
        receive_steering_angle(parent_pipe)  # 메인 함수에서 조향각 수신 및 처리
        rospy.spin()
    except KeyboardInterrupt:
        print("프로그램이 중단되었습니다.")
    finally:
        stop_motors_and_steering()
        p.join()

