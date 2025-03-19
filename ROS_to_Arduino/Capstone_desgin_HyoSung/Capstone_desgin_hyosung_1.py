#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy, serial
from sensor_msgs.msg import LaserScan
import math

import signal
import sys
import os

#lidar_module----------------------------------
import lidar_12m, lidar_10m, lidar_5m, lidar_1m
import array_set as aset
import detect
#----------------------------------------------

def signal_handler(sig, frame):
    import time
    time.sleep(3)
    os.system('killall -9 python rosout')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

range = 0

def RAD2DEG(x):
    return x * 180.0 / math.pi

def scanCallback(scan):

    global range, seridev

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
                range = dist_1
                seridev.write(range)
                print(f'Obstacle detected {dist_1:.1f} ~ {dist_2:.1f} meters ahead, directly in front. Prepare to decelerate.')
            else:
                 print('No object on your front')
        else:
            print('result is None')

def main():

    rospy.init_node("Capstone_Desgin_DT", anonymous = True)
    rospy.Subscriber("/scan", LaserScan, scanCallback)
    rospy.spin()

if __name__ == "__main__":

    global seridev

    try:
        seridev = serial.Serial('/dev/ttyTaeHee', 9600)
        main()
    except rospy.ROSInterruptException:
        pass    

    