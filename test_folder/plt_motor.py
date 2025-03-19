#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import math
import time
from multiprocessing import Pipe, Process

# 자식 프로세스 함수 - 파이프를 통해 데이터를 전달
def plt_motor(pipe):
    # 카메라 장치 열기 (/dev/video_left_line)
    cap = cv2.VideoCapture('/dev/video_left_line')

    # 카메라 해상도와 FPS 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 15)

    # 해상도 설정
    width, height = 640, 480

    # 타이머 설정 (각도를 0.5초마다 출력)
    last_print_time = time.time()

    # 파란점 기준 좌표 설정
    left_x_threshold = 190
    right_x_threshold = 450

    # 버드 아이 뷰 변환을 위한 좌표 설정 (좌상, 우상, 우하, 좌하)
    p1 = [20, 350]  # 좌상
    p2 = [620, 350]  # 우상
    p3 = [640, 380]  # 우하
    p4 = [0, 380]  # 좌하

    # 변환 전의 이미지에서의 좌표
    corner_points_arr = np.float32([p1, p2, p3, p4])

    # 변환 후 적용할 좌표 설정 (정사각형 형태로 변환)
    image_p1 = [0, 0]
    image_p2 = [width, 0]
    image_p3 = [width, height]
    image_p4 = [0, height]
    image_params = np.float32([image_p1, image_p2, image_p3, image_p4])

    # 노란색을 인식하기 위한 HSV 범위 설정
    lower_yellow = np.array([10, 70, 70])
    upper_yellow = np.array([40, 255, 255])

    # 마지막으로 출력한 앵글값 저장 (기본값은 None)
    last_left_angle = None
    last_right_angle = None
    manual_steering_active = False  # 수동 조향 제어 상태 플래그
    
    box_start = (100, 370)  # 네모 박스 시작 좌표 (x, y)
    box_end = (540, 450)    # 네모 박스 끝 좌표 (x, y)

    # 윤곽선을 직선으로 변환하기 위한 함수
    def contour_to_line(contour, image_shape):
        rows, cols = image_shape[:2]
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        lefty = int((-x * vy / vx) + y)
        righty = int(((cols - x) * vy / vx) + y)
        return (0, lefty, cols - 1, righty)

    # 윤곽선 위에 짧은 선을 그리기 위한 함수
    def contour_to_short_line(contour, image_shape, length=50):
        rows, cols = image_shape[:2]
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        mid_x = int(x)
        mid_y = int(y)

        # 선의 길이를 제한해서 짧은 선으로 변환
        start_x = max(0, mid_x - length // 2)
        end_x = min(cols - 1, mid_x + length // 2)
        start_y = int(mid_y - (length // 2) * vy / vx)
        end_y = int(mid_y + (length // 2) * vy / vx)
        
        # 선의 중심 좌표 계산 (파란 점을 그릴 위치)
        center_x = (start_x + end_x) // 2
        center_y = (start_y + end_y) // 2
        
        return (start_x, start_y, end_x, end_y, center_x, center_y, vx, vy)

    # 기울기를 각도로 변환하는 함수
    def calculate_slope_angle(vx, vy):
        # 기울기 각도를 계산하고, 보정 값 87을 사용하여 0도 기준으로 맞춘다
        angle_rad = math.atan2(vy, vx)
        angle_deg = math.degrees(angle_rad)
        
        # 87도와 -87도를 0도로 간주하고 보정
        if angle_deg > 87:
            angle_deg = 87
        elif angle_deg < -87:
            angle_deg = -87
        
        # 보정 후 87을 기준으로 0도로 맞추기
        corrected_angle = angle_deg - 87 if angle_deg > 0 else angle_deg + 87
        return int(-corrected_angle)  # 양수는 음수로, 음수는 양수로 변환

    # 파란선과 빨간선 간의 거리를 계산하는 함수
    def calculate_distance_from_center(center_x, blue_line_x):
        return abs(center_x - blue_line_x)

    # 비디오 프레임을 읽어오는 루프
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_resized = cv2.resize(frame, (width, height))
        
        # "Original Frame" 창에만 네모 박스 그리기
        original_frame_with_box = frame_resized.copy()  # 원본 프레임 복사본 생성
        cv2.rectangle(original_frame_with_box, box_start, box_end, (0, 255, 0), 2)
        
        # 네모 박스 안의 영역 추출
        roi = original_frame_with_box[box_start[1]:box_end[1], box_start[0]:box_end[0]]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # 흰색 픽셀 수 계산
        _, thresholded = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)
        white_pixel_count = np.sum(thresholded == 255)
        
        # 흰색 픽셀 수가 3000 이상일 때 'stop' 신호를 메인 파이프로 전송
        if white_pixel_count >= 100000:
            pipe.send(("stop", 0))  # 'stop' 메시지 전송

        # 투영 변환 행렬 계산
        mat = cv2.getPerspectiveTransform(corner_points_arr, image_params)
        
        # 변환 행렬을 사용하여 이미지 변환
        frame_transformed = cv2.warpPerspective(frame_resized, mat, (width, height))
        
        # BGR을 HSV로 변환
        hsv = cv2.cvtColor(frame_transformed, cv2.COLOR_BGR2HSV)
        
        # 노란색 영역을 마스크로 생성
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # 마스크에 가우시안 블러 적용 (윤곽선 더 부드럽게 만들기)
        blurred_mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # 마스크를 사용하여 노란색 차선을 추출
        result = cv2.bitwise_and(frame_transformed, frame_transformed, mask=blurred_mask)

        # 윤곽선 검출 (Contour Detection)
        contours, _ = cv2.findContours(blurred_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        left_angles = []
        right_angles = []

        # 좌우 윤곽선을 별도로 저장할 리스트
        left_lines = []
        right_lines = []

        # 짧은 선을 그리기 위한 프레임 복사본 생성
        frame_with_short_lines = frame_transformed.copy()

        # 윤곽선이 검출된 경우, 직선으로 변환 후 차선 그리기
        if len(contours) > 0:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 8000:  # 작은 점들을 걸러내기 위한 최소 면적 조정
                    # 윤곽선 직선을 Transformed 창에 그리기 (윤곽선용)
                    line_points = contour_to_line(contour, frame_transformed.shape)
                    cv2.line(frame_transformed, (line_points[0], line_points[1]), (line_points[2], line_points[3]), (0, 255, 0), 5)

                    # 짧은 선을 그리는 창 (Short Line Lane Detection 창)
                    short_line_points = contour_to_short_line(contour, frame_transformed.shape, length=50)
                    # 윤곽선 리스트에 추가
                    center_x = short_line_points[4]
                    if center_x < width // 2:
                        left_lines.append(short_line_points)
                    else:
                        right_lines.append(short_line_points)

        # 좌우에 윤곽선이 2개 이상 인식된 경우, 중심에 가장 가까운 선만 그리기 (파란선 기준)
        blue_line_x = frame_with_short_lines.shape[1] // 2
        
        # 왼쪽 윤곽선 처리
        if len(left_lines) > 1:
            left_lines.sort(key=lambda line: calculate_distance_from_center(line[4], blue_line_x))
            left_lines = [left_lines[0]]  # 가장 가까운 선만 남김

        # 오른쪽 윤곽선 처리
        if len(right_lines) > 1:
            right_lines.sort(key=lambda line: calculate_distance_from_center(line[4], blue_line_x))
            right_lines = [right_lines[0]]  # 가장 가까운 선만 남김

        # 남은 좌우 차선 그리기 (파란선과 가까운 선)
        for short_line_points in left_lines + right_lines:
            cv2.line(frame_with_short_lines, (short_line_points[0], short_line_points[1]), 
                     (short_line_points[2], short_line_points[3]), (0, 0, 255), 5)

            # 짧은 선의 중심에 파란 점을 그리기
            center_x, center_y = short_line_points[4], short_line_points[5]
            cv2.circle(frame_with_short_lines, (center_x, center_y), 5, (255, 0, 0), -1)  # 파란 점 그리기

            # 수동 조향각 활성화 조건 확인 및 final_steering_angle 설정
            final_steering_angle = 0  # 최종 조향각 변수
            if center_x < width // 2 and center_x >= left_x_threshold:
                manual_steering_active = True
                final_steering_angle = -20  # 수동 조향각 설정 (왼쪽)
            elif center_x >= width // 2 and center_x <= right_x_threshold:
                manual_steering_active = True
                final_steering_angle = 20  # 수동 조향각 설정 (오른쪽)
            else:
                manual_steering_active = False  # 수동 조향각 비활성화

            # 각도 계산
            vx, vy = short_line_points[6], short_line_points[7]
            slope_angle = calculate_slope_angle(vx, vy)

            if center_x < width // 2:
                left_angles.append(slope_angle)
            else:
                right_angles.append(slope_angle)

        # 차선 인식 및 평균 또는 단일 앵글값 출력
        if not manual_steering_active:
            if left_angles and right_angles:
                avg_left_angle = sum(left_angles) / len(left_angles)
                avg_right_angle = sum(right_angles) / len(right_angles)
                avg_angle = (avg_left_angle + avg_right_angle) / 2
                last_left_angle = int(avg_left_angle)
                last_right_angle = int(avg_right_angle)
                final_steering_angle = avg_angle  # 최종 조향각 계산
            elif left_angles:
                avg_left_angle = sum(left_angles) / len(left_angles)
                last_left_angle = int(avg_left_angle)
                final_steering_angle = avg_left_angle  # 최종 조향각 계산
            elif right_angles:
                avg_right_angle = sum(right_angles) / len(right_angles)
                last_right_angle = int(avg_right_angle)
                final_steering_angle = avg_right_angle  # 최종 조향각 계산
            else:
                # 차선을 인식하지 못했을 때 마지막 앵글값 출력
                if last_left_angle and last_right_angle:
                    avg_angle = (last_left_angle + last_right_angle) / 2
                    final_steering_angle = avg_angle
                elif last_left_angle:
                    final_steering_angle = last_left_angle
                elif last_right_angle:
                    final_steering_angle = last_right_angle
                    
        final_steering_angle *= 1            
                    
        # 파이프에 최종 조향각 전송
        pipe.send((frame_with_short_lines, final_steering_angle))

        # "Short Line Lane Detection" 창 중심에 파란 선을 그리기
        center_x = frame_with_short_lines.shape[1] // 2
        bottom_y = frame_with_short_lines.shape[0]
        line_length = 100
        start_point = (center_x, bottom_y)
        end_point = (center_x, bottom_y - line_length)
        cv2.line(frame_with_short_lines, start_point, end_point, (255, 0, 0), 2)  # 파란선 (중앙선)

        # 원본 프레임 추가 (오리지널 영상을 표시)
        cv2.imshow('Original Frame', original_frame_with_box)  # 네모 박스가 있는 프레임

        # 변환된 프레임을 화면에 출력 (윤곽선 기반 차선 그리기)
        cv2.imshow('Transformed Frame with Lane Detection', frame_transformed)  # 네모 박스 없는 변환된 프레임

        # 짧은 선이 그려진 새로운 창 (중앙에 파란 점 및 가장 가까운 빨간선 추가)
        cv2.imshow('Short Line Lane Detection', frame_with_short_lines)  # 네모 박스 없는 차선 검출 창
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 부모 프로세스: 파이프 생성 및 자식 프로세스 시작
if __name__ == "__main__":
    parent_pipe, child_pipe = Pipe()  # 파이프 생성
    p = Process(target=plt_motor, args=(child_pipe,))  # 자식 프로세스 생성
    p.start()  # 자식 프로세스 시작

    while True:
        if parent_pipe.poll():  # 파이프에 데이터가 있을 때만 읽음
            frame, steering_angle = parent_pipe.recv()
            
            # 여기서 프레임을 표시하거나 다른 작업 수행 가능

        time.sleep(0.1)  # 데이터 수신 주기 (0.1초 간격)

    p.join()  # 자식 프로세스 종료 대기

