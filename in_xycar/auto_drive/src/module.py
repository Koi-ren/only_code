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

close = 0

def drive(angle, speed):
    global pub

    msg = xycar_motor()
    msg.angle = Angle
    msg.speed = Speed

    pub.publish(msg)

def RAD2DEG(x):
    return x * 180.0 / math.pi
def scanCallback(scan):
    global close
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))
    
    len_12_1 = aset.array_mid_1
    len_10_1 = aset.array_mid_2
    len_5_1 = aset.array_mid_3
    len_1_1 = aset.array_mid_4
    
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
                close+=1

        len_12_2 = len(len_12_1)
        len_10_2 = len(len_10_1)
        len_5_2  = len(len_5_1)
        len_1_2  = len(len_1_1)
    return close, len_1_2, len_5_2, len_10_2, len_12_2

def usbcam_callback(data):
    global image
    image = bridge.imgmsg_to_cv2(data, "bgr8")
    return image

def ultra_callback(data):
    global ultra_msg
    ultra_msg = data.data
    return ultra_msg

!def ultra_filtering():
    global ultra_msg

!def drive(angle, speed):
    motor_msg.angle = angle
    motor_msg.speed = speed
    motor.publish(motor_msg)

def stop_car(duration):
    for i in range(int(duration)): 
        stop = drive(angle=0, speed=0)
    return stop

def move_car(move_angle, move_speed, duration):
    for i in range(int(duration)): 
        drive(move_angle, move_speed)
        time.sleep(0.1)