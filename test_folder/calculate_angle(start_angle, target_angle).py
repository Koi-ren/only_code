
while True:
    start_angle = float(input("출발 시점: "))
    target_angle = float(input("도착 시점: "))
    # 시계 방향 각도 차이 계산
    clockwise_diff = (target_angle - start_angle + 360) % 360
    # 반시계 방향 각도 차이 계산
    counterclockwise_diff = (start_angle - target_angle + 360) % 360
    
    # 시계 방향이 더 짧으면 +로 표시 (시계 방향) 
    if clockwise_diff <= counterclockwise_diff:
        print(float(clockwise_diff))
    # 반시계 방향이 더 짧으면 -로 표시 (반시계 방향)
    else:
        print( -float(counterclockwise_diff))