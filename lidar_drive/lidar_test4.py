#!/usr/bin/env python3
#본 코드의 객체 인식 추측 방법: 라이다로 들어오는 각도 및 거리 값을 제한하여 제한 각도 및 제한 거리안에 물체 감지 시 특정 배열에 요소를 추가한다.
#가장 많은 요소를 가진 배열이 소속된 제한 각도를 찾고, 찾은 제한 각도 안에 가장 가깝고 큰 객체가 있을 것이라는 추정
#다만 x축은 고려를 하지 못한다 -> 2d라이다이기 때문. 기기의 한계
#제한 각도를 세분화 하여 프로세서를 구체화 시키는 것이 목표가 될 것.

#본 코드에선 객체 감지 포인트의 수가 30 이하일 경우 노이즈로 간주한다. --> 차후 개선할 것


import rospy
from sensor_msgs.msg import LaserScan
import math

def RAD2DEG(x):
    return x * 180.0 / math.pi
    
def scanCallback(scan):
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))
    
    array_le = []
    array_mid = []
    array_ri = []
    
    for i in range(count):
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        dist = scan.ranges[i]
        if(-180.000000 < degree < -160.000000) and (dist < 1.000000):
            array_mid.append(1)
        
        elif(160.000000 < degree < 180.000000) and (dist < 1.000000):
            array_mid.append(1)
        
        elif(-150.000000 < degree <= -90.000000) and (dist < 1.000000):
            array_le.append(1)
        
        elif(90.000000 <= degree < 150.000000) and (dist < 1.000000):
            array_ri.append(1)
        
    #mco = most_closest_object
    mco = max(len(array_mid), len(array_le), len(array_ri))
    
    if (mco == len(array_mid)) and (mco > 30):
        rospy.loginfo(": The closest object is in front")
        rospy.loginfo("mid:[%d], right:[%d], left:[%d]"%(len(array_mid), len(array_ri), len((array_le))))
    elif (mco == len(array_ri)) and (mco > 30):
        rospy.loginfo(": The closest object is on the right")
        rospy.loginfo("mid:[%d], right:[%d], left:[%d]"%(len(array_mid), len(array_ri), len((array_le))))
    elif (mco == len(array_le)) and (mco > 30):
        rospy.loginfo(": The closest object is on the left")
        rospy.loginfo("mid:[%d], right:[%d], left:[%d]"%(len(array_mid), len(array_ri), len((array_le))))
    elif mco < 30:
        rospy.loginfo(": no object on your side")
        rospy.loginfo("mid:[%d], right:[%d], left:[%d]"%(len(array_mid), len(array_ri), len((array_le))))
        
    array_le = []
    array_mid = []
    array_ri = []
        
    
def main():
    rospy.init_node("rplidar_node_client")
    rospy.Subscriber("/scan", LaserScan, scanCallback)
    rospy.spin()

if __name__ == "__main__":
    main()