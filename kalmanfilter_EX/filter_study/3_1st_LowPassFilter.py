'''
이동 평균 필터의 문제점은 전에 들어왔던 값의 가중치와 
최신화된 데이터의 가중치가 같다는 것에 문제가 있다.

예를들어 150hz의 측정 주기를 가진 센서의 데이터를 필터링한다고 가정하고, 
이동 평균 데이터 개수를 150개로 제한한다면 이 경우 필터에 사용되는 가장 오래된 측정값은
1초 전에 측정값이다.

지속해서 값이 변화하고 있다면 1초 전에 들어온 값의 신뢰도는 떨어진 상태가 된다.

따라서 위의 단점을 보완하고자 고안된 필터가바로 저역 통과 필터(Low-pass-filter)이다.

단점을 보완한 방식으로는 비교적 이전 데이터에 낮은 가중치를, 
최신 데이터에는 높은 가중치를 두는 것으로 한다.

1차 저역 통과 필터를 우리는 지수가중(Exponentially weighted) 이동평균 필터라고 부른다.

여기서 alpha 값이 작을 수록 잡음이 더 많아지고, 커질 수록 잡음은 줄어든 대신 시간지연이 더 커진다.

참고로 alpha값의 범위는 0 < alpha < 1 이다.

alpha 값이 작으면 이전 추정값의 가중치가 낮아지고 측정값의 가중치가 높아지기에 추정값에 측정값이 더 많이 반영됨.
반대로 alpha 값이 커지면 이전추정값의 가중치가 높아지고 측정값의 가중치가 낮아진다
'''

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt

def low_pass_filter(prev_value, new_value, alpha):
    return alpha * prev_value + (1 - alpha) * new_value

if __name__ == "__main__":
    alpha = 0.7  # Low-pass filter coefficient
    num_iterations = 20
    input_values = []
    estimated_values = []
    
    # 첫 번째 입력 값으로 초기화
    initial_value = float(input("초기 값을 입력하시오: "))
    input_values.append(initial_value)
    estimated_values.append(initial_value)
    
    for i in range(1, num_iterations):
        new_value = float(input("추가되는 값: "))
        estimated_value = low_pass_filter(estimated_values[-1], new_value, alpha)
        input_values.append(new_value)
        estimated_values.append(estimated_value)
        print(f"입력 값: {new_value}, 추정 값: {estimated_value}")
    
    # Plot the input and estimated values
    plt.plot(range(num_iterations), input_values, label='Input Values')
    plt.plot(range(num_iterations), estimated_values, label='Estimated Values')
    plt.xlabel('Sample Number')
    plt.ylabel('Value')
    plt.legend()
    plt.title('Input Values and Estimated Values with 1st Order Low-pass Filter Applied')
    plt.show()
