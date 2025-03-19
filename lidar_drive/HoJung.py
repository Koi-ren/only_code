import rospy
from sensor_msgs.msg import LaserScan
import math

NOISE = 30  # 노이즈로 간주할 최소 포인트 수

def RAD2DEG(x):
    return x * 180.0 / math.pi  # 라디안 값을 도 단위로 변환

def isNoise(count):  # 감지된 객체 포인트 수가 노이즈 임계값 이하인지 확인
    return count <= NOISE

def scanCallback(scan):
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))

    # 변수 초기화
    mid_count = 0
    le_count = 0
    ri_count = 0

    # 각 값 미리 계산
    angle_min_deg = RAD2DEG(scan.angle_min)
    angle_increment_deg = RAD2DEG(scan.angle_increment)

    for i in range(count):
        degree = angle_min_deg + angle_increment_deg * i
        dist = scan.ranges[i]

        if dist < 1.0:
            if -180.00 < degree < -160.00 or 160.00 < degree < 180.00:
                mid_count += 1
            elif -150.00 < degree <= -90.00:
                le_count += 1
            elif 90.00 <= degree < 150.00:
                ri_count += 1

    # 가장 많은 객체 인식 포인트를 가진 방향 결정
    mco = max(mid_count, le_count, ri_count)

    # 인식된 객체에 따른 동작 결정
    if isNoise(mco):
        rospy.loginfo(": no object on your side (noisy data)")
    else:
        if mco == mid_count:
            rospy.loginfo(": The closest object is in front")
        elif mco == ri_count:
            rospy.loginfo(": The closest object is on the right")
        elif mco == le_count:
            rospy.loginfo(": The closest object is on the left")

    # 디버깅을 위해 출력
    rospy.loginfo("mid:[%d], right:[%d], left:[%d]" % (mid_count, ri_count, le_count))

def main():
    rospy.init_node("rplidar_node_client")
    rospy.Subscriber("/scan", LaserScan, scanCallback)
    rospy.spin()

if __name__ == "__main__":
    main()