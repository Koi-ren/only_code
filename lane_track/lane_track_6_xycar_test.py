#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math, rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()
image = np.empty(shape=[0])
#===================================
#콜백함수
#===================================
def usbcam_callback(data):
    global image
    image = bridge.imgmsg_to_cv2(data, "bgr8")

#===================================
#새로운 차선 발견 코드
#===================================

width = 320
height = 240


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    channel_count = 3
    match_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=2): # 선 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

rospy.init_node('lane_track')
rospy.Subscriber("/usb_cam/image_raw/",Image,usbcam_callback, queue_size=1)
rospy.wait_for_message("/usb_cam/image_raw/", Image)
print("Camera Ready --------------")
#======================================
#자이카에서 굴러가게 하게 정보를 바꾸는 영역
#======================================
while not rospy.is_shutdown():
    region_of_interest_vertices = [
        (0, height),
        (width / 2, height / 2),
        (width, height),
    ]
    image = image.copy()
    cropped_image = region_of_interest(
        image,
        np.array([region_of_interest_vertices], np.int32),
    )
    
    # Convert to grayscale here.
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)
    # Call Canny Edge Detection here.
    cannyed_image = cv2.Canny(gray_image, 100, 200)
    
    cropped_image = region_of_interest(
        cannyed_image,
        np.array(
            [region_of_interest_vertices],
            np.int32
        ),
    )
    lines = cv2.HoughLinesP(
        cropped_image,
        rho=6,
        theta=np.pi / 60,
        threshold=160,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=25
    )
    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1) # <-- Calculating the slope.
            if math.fabs(slope) < 0.5: # <-- Only consider extreme slope
                continue
            if slope <= 0: # <-- If the slope is negative, left group.
                left_line_x.extend([x1, x2])
                left_line_y.extend([y1, y2])
            else: # <-- Otherwise, right group.
                right_line_x.extend([x1, x2])
                right_line_y.extend([y1, y2])
    line_image = draw_lines(image, lines) # <---- Add this call.
    
    cv2.imshow(line_image)
    cv2.waitKey(1)