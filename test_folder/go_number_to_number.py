# 정해진 값 배열 (순서대로 진행)
target_values = [10, 20, 30, 40, 50]

# 현재 순번을 저장하는 변수
current_index = 0

# 오차 범위
tolerance = 2

# 함수: 입력 값을 처리하는 함수
def process_input(input_value):
    global current_index

    # 정해진 값과 현재 순번의 값을 가져옴
    target_value = target_values[current_index]

    # 입력 값과 정해진 값의 차이가 오차 범위 이내일 때
    if abs(input_value - target_value) <= tolerance:
        print(f"Input {input_value} is close to target {target_value}")
        # 다음 순번으로 넘어감
        current_index += 1
        
        # 마지막 순번을 넘어가지 않도록 처리
        if current_index >= len(target_values):
            print("All target values have been matched.")
            current_index = len(target_values) - 1  # 마지막 순번 고정
    else:
        print(f"Input {input_value} is not within tolerance of target {target_value}")

# 테스트: 입력 값이 순차적으로 주어지는 경우
input_values = [8, 21, 29, 41, 51]  # 예시 입력 값

for value in input_values:
    process_input(value)
