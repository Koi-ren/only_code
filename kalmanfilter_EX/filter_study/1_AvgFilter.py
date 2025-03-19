#그냥 평균 그자체

import sys

Prev_k = 3  # 이전 평균 개수
Prev_Avg = 20  # 이전 평균값

if __name__ == "__main__":
    try:
        while True:  # 무한 반복문

            print(F"이전 평균값: {Prev_Avg} \n시행수: {Prev_k}")
            k = Prev_k + 1  # 현재 평균 개수
            a = Prev_k / k

            x = float(input("추가되는 값: "))

            Avg = Prev_Avg * a + (1 - a) * x
            print(f"새로운 평균값: {Avg}")

            # 이전 평균값과 평균 개수를 업데이트
            Prev_Avg = Avg
            Prev_k = k
    except KeyboardInterrupt:
        print("\n프로그램이 종료되었습니다.")
        sys.exit()
