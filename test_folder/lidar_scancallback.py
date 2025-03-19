right_object, mid_object, left_object, stop_car = False, False, False, False

def scanCallback(scan):
    global close, stop_car, right_object, mid_object, left_object, dist, degree
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))

    right_obj, mid_obj, left_obj, close = 0, 0, 0, 0
    for i in range(count):
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        dist = scan.ranges[i]
        if (165.0 <= degree <= 180.0) or (-180.0 <= degree <= -165.0) and (dist <= 3.0):
                mid_obj += 1
                if dist <= 1.0:
                    close += 1
        if (135.0 <= degree <= 165.0) and (dist <= 3.0):
                right_obj += 1
        if (-165.0 <= degree <= -135) and (dist <= 3.0):
                left_obj += 1

        if right_object >= 93:
            right_object = True
        else: 
            right_object = False
        if mid_obj >= 93:
            mid_object = True
        else:
            mid_object = False
        if left_obj >= 93:
            left_object = True
        else:
            left_object = False 
        if close >= 93:
            stop_car = True
        else: 
            stop_car = False

        if stop_car == True:
            #차멈추기
            pass
        else:
            stop_car == False
             
        
        