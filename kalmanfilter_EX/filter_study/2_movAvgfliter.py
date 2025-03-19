'''
평균의 함정을 피하기 위해 고안된 필터이다.

평균은 결국 시행수가 많아 질 수록 그 정확도는 현저히 떨어지기에

특정 값(이동 평균 데이터 개수)을 통해 평균을 최신화 하여 정확도를 높인다. 
'''

import sys

def moving_average_filter(input_values, new_value, num_values):
    input_values.append(new_value)
    if len(input_values) > num_values:
        input_values.pop(0)
    return sum(input_values) / len(input_values)

if __name__ == "__main__":
    input_values = []
    num = int(input("이동 평균 데이터 개수: "))

    for _ in range(num):
        value = float(input("값을 입력하시오: "))
        input_values.append(value)
    
    while True:
        try:
            new_value = float(input("추가되는 값: "))
            mov_avg = moving_average_filter(input_values, new_value, num)
            print(f"이동 평균: {mov_avg}")
        except KeyboardInterrupt:
            sys.exit()