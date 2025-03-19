#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()
image = np.empty(shape=[0])

def usbcam_callback(data):
    global image
    image = bridge.imgmsg_to_cv2(data, "bgr8")

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def draw_fit_line(img, lines, color=[255, 0, 0], thickness=10):
    if lines is not None:
        cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    return lines

def weighted_img(img, initial_img, a=1, b=1., c=0.):
    return cv2.addWeighted(initial_img, a, img, b, c)

def get_fitline(img, f_lines): # 대표선 구하기   
    lines = np.squeeze(f_lines)
    if len(lines.shape) != 2 or lines.shape[1] != 4:
        return None

    x_coords = lines[:, [0, 2]].reshape(-1)
    y_coords = lines[:, [1, 3]].reshape(-1)

    num_points = len(x_coords)

    if num_points > 0:
        vx, vy, x, y = cv2.fitLine(np.vstack((x_coords, y_coords)).T, cv2.DIST_L2, 0, 0.01, 0.01)

        # 이미지의 하단 경계에서 시작하고, 중간 부분의 y 좌표에서 끝나도록 변경
        y1, y2 = img.shape[0], int(img.shape[0] / 2 + 100)
        x1 = int((y1 - y) / vy * vx + x)
        x2 = int((y2 - y) / vy * vx + x)

        result = [x1, y1, x2, y2]
        return result
    else:
        return None

rospy.init_node('lane_track')
rospy.Subscriber("/usb_cam/image_raw", Image, usbcam_callback, queue_size=1)
rospy.wait_for_message("/usb_cam/image_raw", Image)
print("Camera Ready --------------")

while not rospy.is_shutdown():
    image = image.copy()

    height, width = 480, 640

    gray_img = grayscale(image)
    blur_img = gaussian_blur(gray_img, 3)
    canny_img = canny(blur_img, 70, 210)

    vertices = np.array([[(50, height), (width/2-45, height/2+60), (width/2+45, height/2+60), (width-50, height)]], dtype=np.int32)
    ROI_img = region_of_interest(canny_img, vertices)

    line_arr = hough_lines(ROI_img, 1, np.pi/180, 30, 10, 20)

    if line_arr is not None:
        line_arr = np.squeeze(line_arr)
        slope_degree = (np.arctan2(line_arr[:, 1] - line_arr[:, 3], line_arr[:, 0] - line_arr[:, 2]) * 180) / np.pi
        line_arr = line_arr[np.abs(slope_degree) < 160]
        slope_degree = slope_degree[np.abs(slope_degree) < 160]
        line_arr = line_arr[np.abs(slope_degree) > 95]
        slope_degree = slope_degree[np.abs(slope_degree) > 95]
     
        L_lines, R_lines = line_arr[(slope_degree > 0), :], line_arr[(slope_degree < 0), :]
        temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        L_lines, R_lines = L_lines[:, None], R_lines[:, None]

        left_fit_line = get_fitline(image, L_lines)
        right_fit_line = get_fitline(image, R_lines)
        
        # 좌우 차선만 그리도록 수정
        draw_fit_line(temp, left_fit_line)
        draw_fit_line(temp, right_fit_line)
          
        result = weighted_img(temp, image)
        cv2.imshow('result', result)
        cv2.waitKey(1)

