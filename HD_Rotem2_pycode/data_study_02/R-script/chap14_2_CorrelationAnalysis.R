# chap14_2_Correlation Analysis

######################################################
## Chapter14_2. 상관관계 분석(Correlation Analysis)
######################################################

# 2.2 상관관계 분석 수행 

# [실습] 기술 통계량 구하기 
result <- read.csv("C:/Rwork/Part-III/product.csv", header=TRUE)
head(result) # 친밀도 적절성 만족도(등간척도 - 5점 척도)

# 기술통계량
summary(result) # 요약통계량

sd(result$제품_친밀도); sd(result$제품_적절성); sd(result$제품_만족도)


# [실습] 상관계수(coefficient of correlation) : 두 변량 X,Y 사이의 상관관계 정도를 나타내는 수치(계수)
cor(result$제품_친밀도, result$제품_적절성) # 0.4992086 -> 다소 높은 양의 상관관계
cor(result$제품_친밀도, result$제품_만족도) # 0.467145 -> 다소 높은 양의 상관관계

# [실습] 전체 변수 간 상관계수 보기
cor(result, method="pearson") 

# [실습] 방향성 있는 색생으로 표현  
install.packages("corrgram")   
library(corrgram)
corrgram(result) # 색상 적용 - 동일 색상으로 그룹화 표시
corrgram(result, upper.panel=panel.conf) # 수치(상관계수) 추가(위쪽)
corrgram(result, lower.panel=panel.conf) # 수치(상관계수) 추가(아래쪽)

# [실습] 차트에 밀도 곡선, 상관성, 유의확률(별표) 추가 
install.packages("PerformanceAnalytics") 
library(PerformanceAnalytics) 
# 상관성,p값(*),정규분포 시각화 - 모수 검정 조건 
chart.Correlation(result, histogram=, pch="+") 

# [실습]  spearman : 서열척도 대상 상관계수
cor(result, method="spearman") 
