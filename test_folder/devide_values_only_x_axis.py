from decimal import Decimal, getcontext

# 소수점 자릿수 설정 (15자리)
getcontext().prec = 21

# 시작 값과 끝 값
start_value = Decimal('35.120086703423446')
end_value = Decimal('35.12024819322868')

# 40등분 값 계산
divided_values = [start_value + (end_value - start_value) * Decimal(i) / Decimal(72) for i in range(73)]

# 결과 출력
for value in divided_values:
    for i in divided_values:
    
        print(value)
