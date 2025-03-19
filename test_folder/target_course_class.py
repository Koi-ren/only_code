class TargetCourse:
    """
    목표 경로를 나타내는 클래스입니다.
    """

    def __init__(self, c_lat, c_lon, c_point):
        self.c_lat = c_lat  # 경로의 위도 리스트
        self.c_lon = c_lon  # 경로의 경도 리스트
        self.c_point = c_point  # 각 좌표의 포인트 번호
        self.old_nearest_point_index = None  # 가장 가까운 점의 인덱스 저장
        self.imu_speed = None
        self.point_number = 0  # 현재 포인트 번호
        self.previous_planning_point_number = None  # 이전 포인트 번호 저장

    def search_closest_point(self, state, tolerance=0.001):
        """
        현재 GPS 좌표(state.lat, state.lon)에 가장 근접한 경로 좌표를 검색하고, 포인트 정보 및 방위각을 계산합니다.
        """
        # 가장 가까운 경로 좌표를 찾습니다.
        lat_closest_value = min(self.c_lat, key=lambda x: abs(x - state.lat))
        lon_closest_value = min(self.c_lon, key=lambda x: abs(x - state.lon))

        lat_index = self.c_lat.index(lat_closest_value)
        lon_index = self.c_lon.index(lon_closest_value)

        # 위도와 경도 인덱스가 같을 때, 즉 가장 근접한 경로 좌표를 찾았을 때
        if lat_index == lon_index:
            # 오차 범위 내에 있는지 확인
            if is_within_tolerance(state.lat, state.lon, lat_closest_value, lon_closest_value, tolerance):
                planning_point_number = self.c_point[lat_index]
                self.previous_planning_point_number = planning_point_number
                planning_point_data_bool = True
                print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_closest_value}, 경도: {lon_closest_value}")
            else:
                planning_point_number = self.previous_planning_point_number
                planning_point_data_bool = False
                print("경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
        
        # 위도와 경도 인덱스가 다를 때 각각 처리
        elif lat_index <= lon_index:
            if is_within_tolerance(state.lat, state.lon, lat_closest_value, self.c_lon[lat_index], tolerance):
                planning_point_number = self.c_point[lat_index]
                self.previous_planning_point_number = planning_point_number
                planning_point_data_bool = True
                print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_closest_value}, 경도: {self.c_lon[lat_index]}")
            else:
                planning_point_number = self.previous_planning_point_number
                planning_point_data_bool = False
                print("경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
        
        elif lon_index <= lat_index:
            if is_within_tolerance(state.lat, state.lon, self.c_lat[lon_index], lon_closest_value, tolerance):
                planning_point_number = self.c_point[lon_index]
                self.previous_planning_point_number = planning_point_number
                planning_point_data_bool = True
                print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {self.c_lat[lon_index]}, 경도: {lon_closest_value}")
            else:
                planning_point_number = self.previous_planning_point_number
                planning_point_data_bool = False
                print("경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
        else:
            planning_point_number = self.previous_planning_point_number
            planning_point_data_bool = False
            print("경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
        
        bearing = state.heading_degree
        self.point_number += 1

        # 다음 포인트를 향한 각도 계산
        if planning_point_number + 10 < len(self.c_point):
            target_degree = calculate_bearing(state.rear_lat, state.rear_lon, self.c_lat[planning_point_number], self.c_lon[planning_point_number])
            diff_angle_value = calculate_angle(bearing, target_degree)
        else:
            angle_to_move = 0  # 마지막 포인트에서는 이동 각도 없음

        # 상태 출력
        if not planning_point_data_bool:
            print("현재 가장 가까운 스타팅 포인트로 이동합니다.")
        else:
            print(f"다음 포인트: {planning_point_number + 1}")
        print(f"다음 포인트로 가는 방위 각도: {angle_to_move}")

        return planning_point_number, angle_to_move
