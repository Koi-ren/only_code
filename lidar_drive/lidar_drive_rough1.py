#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from xycar_msgs.msg import xycar_motor
import math


motor = None  # 모터 노드 변수
Fix_Speed = 17  # 모터 속도 고정 상수값 
new_angle = 0  # 모터 조향각 초기값
new_speed = Fix_Speed  # 모터 속도 초기값
motor_msg = xycar_motor()  # 모터 토픽 메시지

def RAD2DEG(x):
    return x * 180.0 / math.pi

#=============================================
# 콜백함수 - 초음파 토픽을 처리하는 콜백함수.
#=============================================
def scanCallback(scan):
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))
    rospy.loginfo("angle_range, %f, %f" % (RAD2DEG(scan.angle_min), RAD2DEG(scan.angle_max)))

    for i in range(count):
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        rospy.loginfo(": [%f, %f]" % (degree, scan.ranges[i]))

#=============================================
# 모터 토픽을 발행하는 함수.  
#=============================================
def drive(angle, speed):
    motor_msg.angle = angle
    motor_msg.speed = speed
    motor.publish(motor_msg)

#=============================================
# 벽과 충돌하지 않으며 주행하도록 핸들 조정함.
#=============================================
def lidar_drive():
    global new_angle, new_speed

    # 앞쪽 가까이에 장애물이 있으면 차량 멈춤
    if (0 < ultra_msg[2] < 20):
        new_angle = new_angle
        new_speed = 0
        print("Car Brake, Stop! : ", ultra_msg)

    # 왼쪽이 오른쪽보다 멀리 있으면 있으면 좌회전 주행
    elif (ultra_msg[1] - ultra_msg[3] > 10):
        new_angle = -50
        new_speed = Fix_Speed
        print("Turn left : ", ultra_msg)

    # 오른쪽이 왼쪽보다 멀리 있으면 있으면 우회전 주행
    elif (ultra_msg[3] - ultra_msg[1] > 10):
        new_angle = 50
        new_speed = Fix_Speed
        print("Turn right : ", ultra_msg)

    # 위 조건에 해당하지 않는 경우라면 (오른쪽과 왼쪽이 비슷한 경우) 똑바로 직진 주행
    else:
        new_angle = 0
        new_speed = Fix_Speed
        print("Go Straight : ", ultra_msg)

    # 모터에 주행명령 토픽을 보낸다
    drive(new_angle, new_speed)


def start():
    global motor
    rospy.init_node("rplidar_node_client")
    motor = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
    rospy.Subscriber("/scan", LaserScan, scanCallback)
    rospy.spin()
    rospy.wait_for_message("lidar_msg", LaserScan)
    print("Lidar Ready-----------")

    while not rospy.is_shutdown():

        lidar_drive()

if __name__ == '__main__':
    start()