while True:
    try:
        # 미리 설정된 값들의 리스트
        predefined_values = [35.119936, 35.1199328, 35.1199264]

        # 키보드로 값 입력 받기
        input_value = float(input("값을 입력하세요: "))

        # 가장 가까운 값 찾기
        closest_value = min(predefined_values, key=lambda x: abs(x - input_value))

        # 결과 출력
        print(f"입력한 값에 가장 근접한 값은: {closest_value}")


    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")
        break