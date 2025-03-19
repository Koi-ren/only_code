/ /lidar 발행 client. cpp을 python파일로 변환한 것.


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
        rospy.loginfo(": [%f, %f]" % (degree, scan.ranges[i]))

def main():
    rospy.init_node("rplidar_node_client")
    rospy.Subscriber("/scan", LaserScan, scanCallback)
    rospy.spin()

if __name__ == "__main__":
    main()