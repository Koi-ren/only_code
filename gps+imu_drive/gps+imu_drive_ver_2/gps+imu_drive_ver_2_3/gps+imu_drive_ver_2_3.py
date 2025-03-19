#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import gps_ins_module_1 as GIM
import time
import csv
import threading
#import numpy as np

lock = threading.Lock()

gps_imu_save_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/gps+imu_coordinates.csv"

with open(gps_imu_save_path, mode='w', newline='') as gps_file:
    gps_writer = csv.writer(gps_file)
    gps_writer.writerow(["Point Number", "Latitude", "Longitude"])

def save_to_csv(file_path, Point_number, Latitude, Longitude):
    """좌표 데이터를 CSV에 저장하는 함수"""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Point_number, Latitude, Longitude])

def main_loop(gps_instance, imu_instance, save_to_csv, gps_imu_save_path):
    i = 0
    prev_lat, prev_lon = None, None
    gps_imu_lat, gps_imu_lon = 0.0, 0.0  # 초기화
    time.sleep(6)  # 초기화 대기 시간

    while True:
        i += 1
        Calc_instance = GIM.Calculation(imu_instance.magnetometer, imu_instance.acceleration, imu_instance.prev_accel)

        part_heading = threading.Thread(target = Calc_instance.heading_degree_found, daemon = True)
        part_calc_dist = threading.Thread(target = Calc_instance.update_velocity_and_distance_trapezoid, daemon = True)

        part_heading.start()
        part_calc_dist.start()
        
        part_heading.join()  # 쓰레드 완료 대기
        part_calc_dist.join()  # 쓰레드 완료 대기
        
        with gps_instance.lock:
            current_lat = gps_instance.lat
            current_lon = gps_instance.lon
        
        if current_lat is not None and current_lon is not None:
            print(f"GPS 좌표: {current_lat}, {current_lon}")
        else:
            print("GPS 신호 수신 못함")

        if prev_lat == current_lat or prev_lon == current_lon:
            plus_imu_lat, plus_imu_lon = Calc_instance.update_position(current_lat)
            gps_imu_lat += plus_imu_lat
            gps_imu_lon += plus_imu_lon

            #소수점 11자리에서 올림 -> folium으로 디버깅할 때 값이 제대로 입력이 안되기 때문
            gps_imu_lat = round(gps_imu_lat, 11)
            gps_imu_lon = round(gps_imu_lon, 11)
            save_to_csv(gps_imu_save_path, i, gps_imu_lat, gps_imu_lon)

        if prev_lat != current_lat or prev_lon != current_lon:
            #imu 데이터 드리프트를 막기위한 속도 및 거리초기화
            Calc_instance.imu_distance[0], Calc_instance.imu_distance[1] = 0, 0
            Calc_instance.imu_velocity[0], Calc_instance.imu_velocity[1] = 0, 0
            #새로운 좌표값에 대응, 이전 위도, 이전 경도, imu로 더할 좌표값 업데이트
            prev_lat, gps_imu_lat, prev_lon, gps_imu_lon = current_lat, current_lat, current_lon, current_lon

        if current_lat is not None and current_lon is not None:
            print(f"gps + imu 좌표: {gps_imu_lat}, {gps_imu_lon}")
        time.sleep(0.00666)

if __name__ == "__main__":

    gps_instance = GIM.gps_part()  # gps_part 인스턴스 생성
    imu_instance = GIM.Imu_part()   # Imu_part 인스턴스 생성
    
    # GPS 및 IMU 스레드 시작
    part_gps = threading.Thread(target = gps_instance.gps_start, daemon = True)
    part_imu = threading.Thread(target = imu_instance.imu_start, daemon = True)

    part_gps.start()
    part_imu.start()

    # 메인 루프 실행
    main_loop(gps_instance, imu_instance, save_to_csv, gps_imu_save_path)