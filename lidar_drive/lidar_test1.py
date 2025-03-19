#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import math

def RAD2DEG(x):
    return x * 180.0 / math.pi

def scanCallback(scan):
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))
    rospy.loginfo("angle_range, %f, %f" % (RAD2DEG(scan.angle_min), RAD2DEG(scan.angle_max)))

    for i in range(count):
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        dist = scan.ranges[i]
        rospy.loginfo(": [%f, %f]" % (degree, dist))
        if(
            (340.0 < degree < 20.0) and (0.0 < dist < 300.0)
        ):
            print('stop')
        elif(
            (300.0 < degree <= 340.0) and (0.0 < dist < 300.0)
        ):
            print('turn right')
        elif(
            (20.0 <= degree < 60.0) and (0.0 < dist < 300.0)
        ):
            print('turn lift') 
        else:
            print('stop')
    
def main():
    rospy.init_node("rplidar_gostop_test")
    rospy.Subscriber("/scan", LaserScan, scanCallback)
    rospy.spin()

if __name__ == "__main__":
    main()