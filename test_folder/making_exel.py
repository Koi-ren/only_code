import pandas as pd

# 입력된 정보
data = {
    "이름": ["홍길동", "이순신", "김유신"],
    "나이": [23, 32, 45],
    "직업": ["학생", "군인", "의사"]
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 엑셀 파일로 저장
df.to_excel("output.xlsx", index=False)

print("엑셀 파일이 생성되었습니다.")