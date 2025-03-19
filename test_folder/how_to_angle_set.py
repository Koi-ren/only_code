# 각도 차이를 구하는 함수
def calculate_angle(start_angle, target_angle):
    # 시계 방향 각도 차이 계산
    clockwise_diff = (target_angle - start_angle + 360) % 360
    # 반시계 방향 각도 차이 계산
    counterclockwise_diff = (start_angle - target_angle + 360) % 360
    
    # 시계 방향이 더 짧으면 +로 표시 (시계 방향)
    if clockwise_diff <= counterclockwise_diff:
        return float(clockwise_diff), '+'
    # 반시계 방향이 더 짧으면 -로 표시 (반시계 방향)
    else:
        return -float(counterclockwise_diff), '-'

# 사용자로부터 각도 입력 받기
start_angle = float(input("출발 각도를 입력하세요 (0 ~ 360도): "))
target_angle = float(input("목표 각도를 입력하세요 (0 ~ 360도): "))

# 각도 계산
angle_to_move, direction_sign = calculate_angle(start_angle, target_angle)

# 결과 출력
print(f"{start_angle}도에서 {target_angle}도로 이동하려면 {direction_sign}{abs(angle_to_move)}도 이동해야 합니다.")
print(f"계산된 각도: {angle_to_move}")
