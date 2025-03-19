import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

# 나눔글꼴 경로 설정
font_path = 'C:\\Windows\\Fonts\\gulim.ttc'

# 폰트 이름 가져오기
font_name = fm.FontProperties(fname=font_path).get_name()

# 폰트 설정
plt.rc('font', family=font_name)

# CSV 파일에서 데이터 불러오기
file_path = 'C:/Users/plane/Desktop/검거까지의 시간.csv'
df = pd.read_csv(file_path,encoding='utf-8')

# 데이터 시각화
plt.figure(figsize=(14, 8))

# 시간 슬롯의 이름 정의
time_slots = ['1일 이내', '2일 이내', '3일 이내', '10일 이내', '1개월 이내', '3개월 이내', '6개월 이내', '1년 이내', '1년 초과', '미상']

# Iterate over each time slot and plot
for idx, row in df.iterrows():
    time_slot = time_slots[idx]
    values = row.iloc[1:].values
    plt.plot(df.columns[1:], values, marker='o', label=time_slot)

# 범례 표시
plt.legend()

# 그래프 제목, x축, y축 라벨 설정
plt.title('검거까지의 시간에 따른 시계열 데이터')
plt.xlabel('년도')
plt.ylabel('값')

plt.show()
