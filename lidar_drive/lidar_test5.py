#!/usr/bin/env python3
#본 코드의 객체 인식 추측 방법: 라이다로 들어오는 각도 및 거리 값을 제한하여 제한 각도 및 제한 거리안에 물체 감지 시 특정 배열에 요소를 추가한다.
#가장 많은 요소를 가진 배열이 소속된 제한 각도를 찾고, 찾은 제한 각도 안에 가장 가깝고 큰 객체가 있을 것이라는 추정
#다만 x축은 고려를 하지 못한다 -> 2d라이다이기 때문. 기기의 한계
#제한 각도를 세분화 하여 프로세서를 구체화 시키는 것이 목표가 될 것.

#본 코드에선 객체 감지 포인트의 수가 30 이하일 경우 노이즈로 간주한다. --> 차후 개선할 것

#기존 if elif else 구조에서 if if if 구조로 변경 -> 조건을 병렬로 처리하여 버리는 값 최소화 --> 안정성 향상

#각도 분해를 20도 단위로 쪼개 


import rospy
from sensor_msgs.msg import LaserScan
import math

def RAD2DEG(x):
    return x * 180.0 / math.pi
    
def scanCallback(scan):
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))

    array_mid = []  #중간
    array_right = []  #오른쪽
    array_left = []  #왼쪽

    #중간 3등분
    array_mid_1 = []
    array_mid_2 = []
    array_mid_3 = []

    #오른쪽 3등분
    array_rig_1 = []
    array_rig_2 = []
    array_rig_3 = []

    #왼쪽 3등분
    array_lef_1 = []
    array_lef_2 = []
    array_lef_3 = []

    #배열 len 값 정리 변수
    mid_1 = 0
    right_1 = 0
    left_1 = 0

    mid_2 = 0
    right_2 = 0
    left_2 = 0


    #라이다가 360도
    for i in range(count):
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        dist = scan.ranges[i]
        
        #----------------------------------------------------------------
        #----------------------------------------------------------------
        #12m-------------------------------------------------------------

        #12m 정면
        if(-178.500000 <= degree < -175.500000) and (10.000000 < dist <= 12.000000):
            array_mid_1.append(1)
        if((-180.000000 <= degree < -178.5000000) or (178.500000 < degree <= 180.000000)) and (10.000000 < dist <= 12.000000):
            array_mid_2.append(1)
        if(175.500000 < degree <= 178.500000) and (10.000000 < dist <= 12.000000):
            array_mid_3.append(1)
        
        #12m 우측
        if(172.500000 < degree <= 175.500000) and (10.000000 < dist <= 12.000000):
            array_rig_1.append(1)
        if(169.500000 < degree <= 172.500000) and (10.000000 < dist <= 12.000000):
            array_rig_2.append(1)
        if(166.500000 < degree <= 169.500000) and (10.000000 < dist <= 12.000000):
            array_rig_3.append(1)

        #12m 좌측
        if(-169.500000 <= degree < -166.500000) and (10.000000 < dist <= 12.000000):
            array_lef_1.append(1)
        if(-172.500000 <= degree < -169.500000) and (10.000000 < dist <= 12.000000):
            array_lef_2.append(1)
        if(-175.500000 <= degree < -172.500000) and (10.000000 < dist <= 12.000000):
            array_lef_3.append(1)
        
        #12m 총정리
        mid_1 = len(array_mid_1) + len(array_mid_2) + len(array_mid_3)
        right_1 = len(array_rig_1) + len(array_rig_2) + len(array_rig_3)
        left_1 = len(array_lef_1) + len(array_lef_2) + len(array_lef_3)
        
        #mid_1, right_1, left_1(이하 mrl_1)에 전우좌 방면 객체 인식 시 원소 추가 
        if(mid_1 >= 9):
            array_mid.append(1)
        if(right_1 >= 9):
            array_right.append(1)
        if(left_1 >= 9):
            array_left.append(1) 
        
        #mid_2, right_2, left_2에 mrl_1의 원소 갯수 저장
        mid_2 = len(array_mid)
        right_2 = len(array_right)
        left_2 = len(array_left)

        if(mid_2 == 1) and (right_2 == 0) and (left_2 == 0):
            rospy.loginfo("Obstacle detected 10 ~ 12 meters ahead, directly in front. Prepare to decelerate.")
        if(mid_2 == 1) and (right_2 == 0) and (left_2 == 1):
            rospy.loginfo("Obstacles detected 10 ~ 12 meters ahead, directly in front and to the left. Execute a right turn.")
        if(mid_2 == 1) and (right_2 == 1) and (left_2 == 0):
            rospy.loginfo("Obstacles detected 10 ~ 12 meters ahead, directly in front and to the right. Execute a left turn.")
        if(mid_2 == 1) and (right_2 == 1) and (left_2 == 1):
            rospy.loginfo("Obstacle detected 10 ~ 12 meters directly ahead. Prepare to stop or execute a right maneuver.")
        if(mid_2 == 0) and (right_2 == 0) and (left_2 == 0):
            rospy.loginfo("No obstacles detected 10 ~ 12 meters ahead. Continue forward.")
        if(mid_2 == 0) and (right_2 == 0) and (left_2 == 1):
            rospy.loginfo("Obstacle detected to the left 10 ~ 12 meters ahead. Maneuver to the right.")
        if(mid_2 == 0) and (right_2 == 1) and (left_2 == 0):
            rospy.loginfo("Obstacle detected to the right 10 ~ 12 meters ahead. Maneuver to the left.")
        if(mid_2 == 0) and (right_2 == 1) and (left_2 == 1):
            rospy.loginfo("Obstacles detected on both left and right sides 10 ~ 12 meters ahead. Prepare for slow movement and maneuvering, prepare for a reverse maneuver.")

        #배열 및 lenth 초기화
        array_mid = []  #중간
        array_right = []  #오른쪽
        array_left = []  #왼쪽

        #중간 3등분
        array_mid_1 = []
        array_mid_2 = []
        array_mid_3 = []

        #오른쪽 3등분
        array_rig_1 = []
        array_rig_2 = []
        array_rig_3 = []

        #왼쪽 3등분
        array_lef_1 = []
        array_lef_2 = []
        array_lef_3 = []

        #배열 len 값 정리 변수
        mid_1 = 0
        right_1 = 0
        left_1 = 0

        mid_2 = 0
        right_2 = 0
        left_2 = 0

        #12m-------------------------------------------------------------
        #----------------------------------------------------------------
        #10m-------------------------------------------------------------

        #10m 정면
        if(-178.500000 <= degree < -175.500000) and (5.000000 < dist <= 10.000000):
            array_mid_1.append(1)
        if((-180.000000 <= degree < -178.5000000) or (178.500000 < degree <= 180.000000)) and (5.000000 < dist <= 10.000000):
            array_mid_2.append(1)
        if(175.500000 < degree <= 178.500000) and (5.000000 < dist <= 10.000000):
            array_mid_3.append(1)
        
        #10m 우측
        if(172.500000 < degree <= 175.500000) and (5.000000 < dist <= 10.000000):
            array_rig_1.append(1)
        if(169.500000 < degree <= 172.500000) and (5.000000 < dist <= 10.000000):
            array_rig_2.append(1)
        if(166.500000 < degree <= 169.500000) and (5.000000 < dist <= 10.000000):
            array_rig_3.append(1)

        #10m 좌측
        if(-169.500000 <= degree < -166.500000) and (5.000000 < dist <= 10.000000):
            array_lef_1.append(1)
        if(-172.500000 <= degree < -169.500000) and (5.000000 < dist <= 10.000000):
            array_lef_2.append(1)
        if(-175.500000 <= degree < -172.500000) and (5.000000 < dist <= 10.000000):
            array_lef_3.append(1)
        
        #10m 총정리
        mid_1 = len(array_mid_1) + len(array_mid_2) + len(array_mid_3)
        right_1 = len(array_rig_1) + len(array_rig_2) + len(array_rig_3)
        left_1 = len(array_lef_1) + len(array_lef_2) + len(array_lef_3)
        
        #mid_1, right_1, left_1(이하 mrl_1)에 전우좌 방면 객체 인식 시 원소 추가 
        if(mid_1 >= 9):
            array_mid.append(1)
        if(right_1 >= 9):
            array_right.append(1)
        if(left_1 >= 9):
            array_left.append(1) 
        
        #mid_2, right_2, left_2에 mrl_1의 원소 갯수 저장
        mid_2 = len(array_mid)
        right_2 = len(array_right)
        left_2 = len(array_left)

        if(mid_2 == 1) and (right_2 == 0) and (left_2 == 0):
            rospy.loginfo("Obstacle detected 5 ~ 10 meters ahead, directly in front. Prepare to decelerate.")
        if(mid_2 == 1) and (right_2 == 0) and (left_2 == 1):
            rospy.loginfo("Obstacles detected 5 ~ 10 meters ahead, directly in front and to the left. Execute a right turn.")
        if(mid_2 == 1) and (right_2 == 1) and (left_2 == 0):
            rospy.loginfo("Obstacles detected 5 ~ 10 meters ahead, directly in front and to the right. Execute a left turn.")
        if(mid_2 == 1) and (right_2 == 1) and (left_2 == 1):
            rospy.loginfo("Obstacle detected 5 ~ 10 meters directly ahead. Prepare to stop or execute a right maneuver.")
        if(mid_2 == 0) and (right_2 == 0) and (left_2 == 0):
            rospy.loginfo("No obstacles detected 5 ~ 10 meters ahead. Continue forward.")
        if(mid_2 == 0) and (right_2 == 0) and (left_2 == 1):
            rospy.loginfo("Obstacle detected to the left 5 ~ 10 meters ahead. Maneuver to the right.")
        if(mid_2 == 0) and (right_2 == 1) and (left_2 == 0):
            rospy.loginfo("Obstacle detected to the right 5 ~ 10 meters ahead. Maneuver to the left.")
        if(mid_2 == 0) and (right_2 == 1) and (left_2 == 1):
            rospy.loginfo("Obstacles detected on both left and right sides 5 ~ 10 meters ahead. Prepare for slow movement and maneuvering, prepare for a reverse maneuver.")

        #배열 및 lenth 초기화
        array_mid = []  #중간
        array_right = []  #오른쪽
        array_left = []  #왼쪽

        #중간 3등분
        array_mid_1 = []
        array_mid_2 = []
        array_mid_3 = []

        #오른쪽 3등분
        array_rig_1 = []
        array_rig_2 = []
        array_rig_3 = []

        #왼쪽 3등분
        array_lef_1 = []
        array_lef_2 = []
        array_lef_3 = []

        #배열 len 값 정리 변수
        mid_1 = 0
        right_1 = 0
        left_1 = 0

        mid_2 = 0
        right_2 = 0
        left_2 = 0

        #10m-------------------------------------------------------------
        #----------------------------------------------------------------
        #5m--------------------------------------------------------------

        #5m 정면
        if(-178.500000 <= degree < -175.500000) and (1.000000 < dist <= 5.000000):
            array_mid_1.append(1)
        if((-180.000000 <= degree < -178.5000000) or (178.500000 < degree <= 180.000000)) and (1.000000 < dist <= 5.000000):
            array_mid_2.append(1)
        if(175.500000 < degree <= 178.500000) and (1.000000 < dist <= 5.000000):
            array_mid_3.append(1)
        
        #5m 우측
        if(172.500000 < degree <= 175.500000) and (1.000000 < dist <= 5.000000):
            array_rig_1.append(1)
        if(169.500000 < degree <= 172.500000) and (1.000000 < dist <= 5.000000):
            array_rig_2.append(1)
        if(166.500000 < degree <= 169.500000) and (1.000000 < dist <= 5.000000):
            array_rig_3.append(1)

        #5m 좌측
        if(-169.500000 <= degree < -166.500000) and (1.000000 < dist <= 5.000000):
            array_lef_1.append(1)
        if(-172.500000 <= degree < -169.500000) and (1.000000 < dist <= 5.000000):
            array_lef_2.append(1)
        if(-175.500000 <= degree < -172.500000) and (1.000000 < dist <= 5.000000):
            array_lef_3.append(1)
        
        #5m 총정리
        mid_1 = len(array_mid_1) + len(array_mid_2) + len(array_mid_3)
        right_1 = len(array_rig_1) + len(array_rig_2) + len(array_rig_3)
        left_1 = len(array_lef_1) + len(array_lef_2) + len(array_lef_3)
        
        #mid_1, right_1, left_1(이하 mrl_1)에 전우좌 방면 객체 인식 시 원소 추가 
        if(mid_1 >= 27):
            array_mid.append(1)
        if(right_1 >= 27):
            array_right.append(1)
        if(left_1 >= 27):
            array_left.append(1) 
        
        #mid_2, right_2, left_2에 mrl_1의 원소 갯수 저장
        mid_2 = len(array_mid)
        right_2 = len(array_right)
        left_2 = len(array_left)

        if(mid_2 == 1) and (right_2 == 0) and (left_2 == 0):
            rospy.loginfo("Obstacle detected 1 ~ 5 meters ahead, directly in front. Prepare to decelerate.")
        if(mid_2 == 1) and (right_2 == 0) and (left_2 == 1):
            rospy.loginfo("Obstacles detected 1 ~ 5 meters ahead, directly in front and to the left. Execute a right turn.")
        if(mid_2 == 1) and (right_2 == 1) and (left_2 == 0):
            rospy.loginfo("Obstacles detected 1 ~ 5 meters ahead, directly in front and to the right. Execute a left turn.")
        if(mid_2 == 1) and (right_2 == 1) and (left_2 == 1):
            rospy.loginfo("Obstacle detected 1 ~ 5 meters directly ahead. Prepare to stop or execute a right maneuver.")
        if(mid_2 == 0) and (right_2 == 0) and (left_2 == 0):
            rospy.loginfo("No obstacles detected 1 ~ 5 meters ahead. Continue forward.")
        if(mid_2 == 0) and (right_2 == 0) and (left_2 == 1):
            rospy.loginfo("Obstacle detected to the left 1 ~ 5 meters ahead. Maneuver to the right.")
        if(mid_2 == 0) and (right_2 == 1) and (left_2 == 0):
            rospy.loginfo("Obstacle detected to the right 1 ~ 5 meters ahead. Maneuver to the left.")
        if(mid_2 == 0) and (right_2 == 1) and (left_2 == 1):
            rospy.loginfo("Obstacles detected on both left and right sides 1 ~ 5 meters ahead. Prepare for slow movement and maneuvering, prepare for a reverse maneuver.")

        #배열 및 lenth 초기화
        array_mid = []  #중간
        array_right = []  #오른쪽
        array_left = []  #왼쪽

        #중간 3등분
        array_mid_1 = []
        array_mid_2 = []
        array_mid_3 = []

        #오른쪽 3등분
        array_rig_1 = []
        array_rig_2 = []
        array_rig_3 = []

        #왼쪽 3등분
        array_lef_1 = []
        array_lef_2 = []
        array_lef_3 = []

        #배열 len 값 정리 변수
        mid_1 = 0
        right_1 = 0
        left_1 = 0

        mid_2 = 0
        right_2 = 0
        left_2 = 0

        #5m-------------------------------------------------------------
        #----------------------------------------------------------------
        #1m--------------------------------------------------------------

        #1m 정면
        if(-175.670000 <= degree < -167.340000) and (0.500000 < dist <= 1.000000):
            array_mid_1.append(1)
        if((-180.000000 <= degree < -175.6700000) or (175.670000 < degree <= 180.000000)) and (0.500000 < dist <= 1.000000):
            array_mid_2.append(1)
        if(167.340000 < degree <= 175.670000) and (0.500000 < dist <= 1.000000):
            array_mid_3.append(1)
        
        #1m 우측(8.33씩 감소)
        if(142.350000 < degree <= 150.680000) and (0.500000 < dist <= 1.000000):
            array_rig_1.append(1)
        if(150.680000 < degree <= 159.010000) and (0.500000 < dist <= 1.000000):
            array_rig_2.append(1)
        if(159.010000 < degree <= 167.340000) and (0.500000 < dist <= 1.000000):
            array_rig_3.append(1)

        #1m 좌측
        if(-159.010000 <= degree < -142.350000) and (0.500000 < dist <= 1.000000):
            array_lef_1.append(1)
        if(-159.010000 <= degree < -167.340000) and (0.500000 < dist <= 1.000000):
            array_lef_2.append(1)
        if(-167.340000 <= degree < -159.010000) and (0.500000 < dist <= 1.000000):
            array_lef_3.append(1)

        #이하로 복붙만 해놓은 상태 수정 요함
        
        #1m 총정리
        mid_1 = len(array_mid_1) + len(array_mid_2) + len(array_mid_3)
        right_1 = len(array_rig_1) + len(array_rig_2) + len(array_rig_3)
        left_1 = len(array_lef_1) + len(array_lef_2) + len(array_lef_3)
        
        #mid_1, right_1, left_1(이하 mrl_1)에 전우좌 방면 객체 인식 시 원소 추가 
        if(mid_1 >= 27):
            array_mid.append(1)
        if(right_1 >= 27):
            array_right.append(1)
        if(left_1 >= 27):
            array_left.append(1) 
        
        #mid_2, right_2, left_2에 mrl_1의 원소 갯수 저장
        mid_2 = len(array_mid)
        right_2 = len(array_right)
        left_2 = len(array_left)

        if(mid_2 == 1) and (right_2 == 0) and (left_2 == 0):
            rospy.loginfo("Obstacle detected 1 ~ 5 meters ahead, directly in front. Prepare to decelerate.")
        if(mid_2 == 1) and (right_2 == 0) and (left_2 == 1):
            rospy.loginfo("Obstacles detected 1 ~ 5 meters ahead, directly in front and to the left. Execute a right turn.")
        if(mid_2 == 1) and (right_2 == 1) and (left_2 == 0):
            rospy.loginfo("Obstacles detected 1 ~ 5 meters ahead, directly in front and to the right. Execute a left turn.")
        if(mid_2 == 1) and (right_2 == 1) and (left_2 == 1):
            rospy.loginfo("Obstacle detected 1 ~ 5 meters directly ahead. Prepare to stop or execute a right maneuver.")
        if(mid_2 == 0) and (right_2 == 0) and (left_2 == 0):
            rospy.loginfo("No obstacles detected 1 ~ 5 meters ahead. Continue forward.")
        if(mid_2 == 0) and (right_2 == 0) and (left_2 == 1):
            rospy.loginfo("Obstacle detected to the left 1 ~ 5 meters ahead. Maneuver to the right.")
        if(mid_2 == 0) and (right_2 == 1) and (left_2 == 0):
            rospy.loginfo("Obstacle detected to the right 1 ~ 5 meters ahead. Maneuver to the left.")
        if(mid_2 == 0) and (right_2 == 1) and (left_2 == 1):
            rospy.loginfo("Obstacles detected on both left and right sides 1 ~ 5 meters ahead. Prepare for slow movement and maneuvering, prepare for a reverse maneuver.")

        #배열 및 lenth 초기화
        array_mid = []  #중간
        array_right = []  #오른쪽
        array_left = []  #왼쪽

        #중간 3등분
        array_mid_1 = []
        array_mid_2 = []
        array_mid_3 = []

        #오른쪽 3등분
        array_rig_1 = []
        array_rig_2 = []
        array_rig_3 = []

        #왼쪽 3등분
        array_lef_1 = []
        array_lef_2 = []
        array_lef_3 = []

        #배열 len 값 정리 변수
        mid_1 = 0
        right_1 = 0
        left_1 = 0

        mid_2 = 0
        right_2 = 0
        left_2 = 0

 
        

        
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
