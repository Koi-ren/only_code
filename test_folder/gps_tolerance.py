def is_within_tolerance(lat1, lon1, lat_target, lon_target, tolerance):
    """주어진 좌표가 목표 좌표의 오차 범위 내에 있는지 확인합니다."""
    distance = calculate_distance(lat1, lon1, lat_target, lon_target)
    return distance <= tolerance

while True:
    try:
        # 아두이노로부터 데이터 읽기
        lat1, lon1, alt1 = read_gps_data(ser)

        # GPS 데이터가 유효한지 확인
        if lat1 is not None and lon1 is not None:
            avg_lat, avg_lon, avg_alt = lat1, lon1, alt1

            # 가장 가까운 위도와 경도 값을 찾습니다.
            lat_closest_value = min(lat_data, key=lambda x: abs(x - lat1))
            lon_closest_value = min(lon_data, key=lambda x: abs(x - lon1))

            lat_index = lat_data[lat_data == lat_closest_value].index[0]
            lon_index = lon_data[lon_data == lon_closest_value].index[0]

            if lat_index == lon_index:
                # 현재 GPS 좌표가 계획된 좌표의 오차 범위 내에 있는지 확인합니다.
                if is_within_tolerance(lat1, lon1, lat_closest_value, lon_closest_value, tolerance):
                    planning_point_number = planning_point_data[lat_index]
                    previous_planning_point_number = planning_point_number
                    planning_point_data_bool = True
                    print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_closest_value}, 경도: {lon_closest_value}")
                else:
                    planning_point_number = previous_planning_point_number
                    planning_point_data_bool = False
                    print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
            else:
                planning_point_number = previous_planning_point_number
                planning_point_data_bool = False
                print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")

            # 기존 코드에 대한 처리 및 명령 전송
            # ...

    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")
        break

    except Exception as e:
        print(f"오류 발생: {e}")
        continue
