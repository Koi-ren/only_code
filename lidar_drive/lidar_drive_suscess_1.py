#!/usr/bin/env python3
# -*- coding: utf-8 -*- 2

import rospy
from std_msgs.msg import Int32MultiArray
from xycar_motor.msg import xycar_motor

from sensor_msgs.msg import LaserScan
import math

#lidar_module----------------------------------
import lidar_12m, lidar_10m, lidar_5m, lidar_1m
import array_set as aset
import detect
#----------------------------------------------


#=============================================
# ÇÁ·Î±×·¥¿¡¼­ »ç¿ëÇÒ º¯¼ö, ÀúÀå°ø°£ ¼±¾ðºÎ
#=============================================
motor = None  # ¸ðÅÍ ³ëµå º¯¼ö
Fix_Speed = 17  # ¸ðÅÍ ¼Óµµ °íÁ¤ »ó¼ö°ª 
new_angle = 0  # ¸ðÅÍ Á¶Çâ°¢ ÃÊ±â°ª
new_speed = Fix_Speed  # ¸ðÅÍ ¼Óµµ ÃÊ±â°ª
motor_msg = xycar_motor()  # ¸ðÅÍ ÅäÇÈ ¸Þ½ÃÁö
di = None

#=============================================
# ÄÝ¹éÇÔ¼ö - ÃÊÀ½ÆÄ ÅäÇÈÀ» Ã³¸®ÇÏ´Â ÄÝ¹éÇÔ¼ö.
#=============================================
def RAD2DEG(x):
    return x * 180.0 / math.pi
def scanCallback(scan):
    global di
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))
    
    len_12_1 = aset.array_mid_1
    len_10_1 = aset.array_mid_2
    len_5_1 = aset.array_mid_3
    len_1_1 = aset.array_mid_4
    di = 0
    
    for i in range(count):
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        dist = scan.ranges[i]

        if (165.000000 <= degree <= 180.000000) or (-180.000000 <= degree < -165.000000):
            if (0.500000 < dist <= 1.000000):
                len_1_1 = lidar_1m.detect(degree)
            elif (1.000000 < dist <= 5.000000):
                len_5_1 = lidar_5m.detect(degree)
            elif (5.000000 < dist <= 10.000000):
                len_10_1 = lidar_10m.detect(degree)
            elif (10.000000 < dist <= 12.000000):
                len_12_1 = lidar_12m.detect(degree)
            else:
                di+=1
             
                                     
        len_12_2 = len(len_12_1)
        len_10_2 = len(len_10_1)
        len_5_2 = len(len_5_1)
        len_1_2 = len(len_1_1)
    print(f"len_12_2 = {len_12_2}")
    print(f"len_10_2 = {len_10_2}")
    print(f"len_5_2 = {len_5_2}")
    print(f"len_1_2 = {len_1_2}")
    print(f"di = {di}")
    if di >=1:
        print("so close")
    else:
    
        #객체의 크기는 10cm + α 로 설정.
        result = detect.judge(len_12_2, len_10_2, len_5_2, len_1_2)
    
        if result is not None:
            dist_1, dist_2 = result
            if 0.5 <= dist_1 and 1.0 <= dist_2:
                print(f'Obstacle detected {dist_1:.1f} ~ {dist_2:.1f} meters ahead, directly in front. Prepare to decelerate.')
            else:
                 print('No object on your front')
        else:
            print('result is None')


#=============================================
# ¸ðÅÍ ÅäÇÈÀ» ¹ßÇàÇÏ´Â ÇÔ¼ö.  
#=============================================
def drive(angle, speed):
    motor_msg.angle = angle
    motor_msg.speed = speed
    motor.publish(motor_msg)
    
#=============================================
# º®°ú Ãæµ¹ÇÏÁö ¾ÊÀ¸¸ç ÁÖÇàÇÏµµ·Ï ÇÚµé Á¶Á¤ÇÔ.
#=============================================
def lidar_drive():
    global new_angle, new_speed, di

    # ¾ÕÂÊ °¡±îÀÌ¿¡ Àå¾Ö¹°ÀÌ ÀÖÀ¸¸é Â÷·® ¸ØÃã
    if di >=1:
        new_angle = new_angle
        new_speed = 0
        print("Car Brake, Stop! ")

    # ¿ÞÂÊÀÌ ¿À¸¥ÂÊº¸´Ù ¸Ö¸® ÀÖÀ¸¸é ÀÖÀ¸¸é ÁÂÈ¸Àü ÁÖÇà
    else:
        new_angle = 0
        new_speed = Fix_Speed
        print("Go Straight ")

    # ¸ðÅÍ¿¡ ÁÖÇà¸í·É ÅäÇÈÀ» º¸³½´Ù
    drive(new_angle, new_speed)

#=============================================
# ½ÇÁúÀûÀÎ ¸ÞÀÎÇÔ¼ö 
#=============================================
def start():
    global motor
    
    #=========================================
    # ³ëµå¸¦ »ý¼ºÇÏ°í, ±¸µ¶/¹ßÇàÇÒ ÅäÇÈµéÀ» ¼±¾ðÇÕ´Ï´Ù.
    #=========================================
    rospy.init_node('lidar_driver')
    motor = rospy.Publisher('xycar_motor', xycar_motor, queue_size=10)
    rospy.Subscriber("/scan", LaserScan, scanCallback)
    #=========================================
    # Ã¹¹øÂ° ÅäÇÈÀÌ µµÂøÇÒ ¶§±îÁö ±â´Ù¸³´Ï´Ù.
    #=========================================
    rospy.wait_for_message("/scan", LaserScan)
    print("lidar Ready ----------")

    while not rospy.is_shutdown():

        # ÃÊÀ½ÆÄ ¼¾¼­·Î ÁÖÇàÇÕ´Ï´Ù.
        lidar_drive()

#=============================================
# ¸ÞÀÎÇÔ¼ö - ¿©±â¼­ start() ÇÔ¼ö È£Ãâ
#=============================================
if __name__ == '__main__':
    start()
