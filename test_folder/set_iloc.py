import pandas as pd

# 데이터프레임 생성
data = {'name': ['John', 'Anna', 'Peter', 'Linda'],
        'age': [24, 23, 22, 21],
        'city': ['New York', 'Paris', 'London', 'Berlin']}
df = pd.DataFrame(data)

# 1번째(0부터 시작) 행의 데이터를 선택
print(df.iloc[1,2])
