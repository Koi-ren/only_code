# chap11_Descriptive Statistics

##################################################
## Chapter11. 기술통계(Descriptive Statistics) 
##################################################

## 1. 기술통계(Descriptive Statistics) 개요  

# 대푯값 : 평균(Mean), 합계(Sum), 중위수(Median), 최빈수(mode), 사분위수(quartile) 등
# 산포도 : 분산(Variance), 표준편차(Standard deviation), 최소값(Minimum), 최대값(Maximum), 범위(Range) 등 
# 비대칭도 : 왜도(Skewness), 첨도(Kurtosis)


## 2. 척도별 기술 통계량 구하기

# 실습 데이터 셋 가져오기
setwd("c:/Rwork/Part-III")
data <- read.csv("descriptive.csv", header=TRUE)
head(data) # 데이터셋 확인

# 데이터 특성 보기
dim(data) # 행(300)과 열(8) 정보 - 차원보기
length(data) # 열(8) 길이
length(data$survey) #survey 컬럼의 관찰치 
str(data) # 데이터 구조보기 -> 데이터 종류,행/열,data
str(data$survey) 

# 데이터 특성(최소,최대,평균,분위수,노이즈-NA) 제공
summary(data) 

# 2.1 명목척도 기술 통계량 
length(data$gender)
summary(data$gender) # 최소,최대,중위수,평균-의미없음
table(data$gender) # 각 성별 빈도수 - outlier 확인-> 0, 5

# 이상치(outlier) 제거 
data <- subset(data,data$gender == 1 | data$gender == 2) # 성별 outlier 제거
x <- table(data$gender) # 성별에 대한 빈도수 저장
x # outlier 제거 확인
barplot(x) # 범주형(명목/서열척도) 시각화 -> 막대차트

# 구성비율 계산 
prop.table(x) # 비율 계산 : 0< x <1 사이의 값
y <-  prop.table(x)
round(y*100, 2) #백분율 적용(소수점 2자리)

# 2.2 서열척도 기술 통계량 
length(data$level) # 학력수준 - 서열
summary(data$level) # 명목척도와 함께 의미없음
table(data$level)  # 빈도분석 - 의미있음

# [실습] 학력 수준(level) 변수의 빈도수 시각화
x1 <- table(data$level) # 각 학력수준에 빈도수 저장
barplot(x1) # 명목/서열척도 -> 막대차트


# 2.3 등간척도 기술 통계량 

# [실습] 만족도(survey) 변수 대상 요약통계량 구하기 
survey <- data$survey
survey

summary(survey) # 만족도(5점 척도)인 경우 의미 있음 -> 2.6(평균이상)
x1<-table(survey) # 빈도수
x1

hist(survey) # 등간척도 시각화 -> 히스토그림
pie(x1)


# 2.4 비율척도 기술 통계량 

# [실습] 생활비(cost) 변수 대상 요약 통계량 구하기  
length(data$cost)
summary(data$cost) # 요약통계량 - 의미있음(mean) - 8.784

# [실습] 데이터 정제[결측치 제거]
plot(data$cost)
data <- subset(data,data$cost >= 2 & data$cost <= 10) # 총점기준
data
x <- data$cost
mean(x) 

# [실습]  평균이 극단치에 영향을 받는 경우 - 중위수(median) 대체
median(x) # 5.4  


# (1) 대표값 구하기 

# [실습] 생활비(cost) 변수 대상 대표값 구하기 
mean(x)
median(x)
sort(x) # 오름차순 
sort(x, decreasing=T) # 내림차순  

# [실습] 생활비(cost) 변수 대상 사분위수 구하기 
quantile(x, 1/4)
quantile(x, 2/4)
quantile(x, 3/4)
quantile(x, 4/4)

# [실습] 생활비(cost) 변수의 최빈수 구하기 
length(x)
x.t <- table(x)
x.t
max(table(x))

x.m <- rbind(x.t)
x.m
class(x.m)
str(x.m)
which(x.m[1, ] == 19)

x.df <- as.data.frame(x.m)
which(x.df[1, ] == 18)
x.df[1, 19]
attributes(x.df)
names(x.df[19])


# (2) 산포도 구하기 

# [실습] 생활비(cost) 변수 대상 산포도 구하기 
var(x) # 분산
sd(x) # 표준편차는 분산의 양의 제곱근
sqrt(var(x))
# 표준편차 -> 분산 
sd(x) ** 2

# (3) 표본분산과 표본 표준편차 


# (4) 빈도분석  

# [실습] 생활비(cost) 변수의 빈도분석과 시각화 
table(data$cost)

hist(data$cost)      # 히스토그램 시각화  
plot(data$cost)      # 산점도 시각화

data$cost2[data$cost >=1 & data$cost <=3] <- 1 
data$cost2[data$cost >=4 & data$cost <=6] <- 2
data$cost2[data$cost >=7] <- 3

table(data$cost2)
barplot(table(data$cost2))
pie(table(data$cost2))


# 2.5 비대칭도 구하기  
install.packages("moments")  # 왜도/첨도 위한 패키지 설치   
library(moments)
cost <- data$cost # 정제된 data
cost
# 왜도 - 평균을 중심으로 기울어진 정도
skewness(cost) 

#첨도 - 표준정규분포와 비교하여 얼마나 뽀족한가 측정 지표
kurtosis(cost) # 2.683438     

# 기본 히스토그램 
hist(cost)

# [실습] 히스토그램 확률밀도/표준정규분포 곡선 
hist(cost, freq = F)
# 확률밀도 분포 곡선 
lines(density(cost), col='blue')
# 표준정규분포 곡선 
x <- seq(0, 8, 0.1)
curve( dnorm(x, mean(cost), sd(cost)), col='red', add = T)



# [실습] attach()/detach() 함수로 기술 통계량 구하기 
attach(data) #data를 붙여라! -> data$ 생략     
length(cost)
summary(cost) # 요약통계량 - 의미있음(mean)
mean(cost) # 가장 의미있음
min(cost)
max(cost)
range(cost) # min ~ max
sd<- sd(cost, na.rm=T)
var(cost, na.rm=T)
sqrt(var(cost, na.rm=T))
sd(cost, na.rm=T)

shapiro.test(cost)

sort(cost) # 오름차순 
sort(cost, decreasing=T) # 내림차순
detach(data) # attach(data) 해제

# [실습] NA가 있는 경우 제거 후 기술 통계량 구하기 
test <-c(1:5,NA,10:20)
min(test) # NA 출력
max(test) # NA 출력
range(test) # NA 출력
mean(test) # NA 출력     

# 결측치 데이터 제거 후 통계량 구함
min(test, na.rm=T) # na.rm=T 결측데이터 제거 방법1
max(test, na.rm=T)
range(test, na.rm=T) 
mean(test, na.rm=T)


##  3. 패키지 이용 기술 통계량 구하기

# 3.1 Hmisc 패키지 이용 
install.packages("Hmisc") # 웹사이트 접속하여 패키지 설치
library(Hmisc) # 해당 패키지를 메모리 로딩

# 전체 변수 대상 기술통계량 제공 - 빈도와 비율 데이터 일괄 수행
describe(data) # Hmisc 패키지에서 제공되는 함수

# 개별 변수 기술통계량
describe(data$gender) # 특정 변수(명목) 기술통계량 - 비율 제공
describe(data$age) # 특정 변수(비율) 기술통계량 - lowest, highest
summary(data$age)


# 3.2 prettyR 패키지 이용 
install.packages("prettyR")
library(prettyR)

# 전체 변수 대상      
freq(data) # 각 변수별 : 빈도, 결측치, 백분율, 특징-소수점 제공
# 개별 변수 대상
freq(data$gender) # 빈도와 비율 제공


# 4. 기술 통계량 보고서 작성

# 4.1 기술 통계량 구하기 

# [실습] 변수 리코딩과 빈도분석 

# 1) 거주지역 변수 리코딩과 비율계산
data$resident2[data$resident == 1] <-"특별시"
data$resident2[data$resident >=2 & data$resident <=4] <-"광역시"
data$resident2[data$resident == 5] <-"시구군"

x<- table(data$resident2)
x
prop.table(x) # 비율 계산 : 0< x <1 사이의 값
y <-  prop.table(x)
round(y*100, 2) #백분율 적용(소수점 2자리)

# 2) 성별 변수 리코딩과 비율계산
data$gender2[data$gender== 1] <-"남자"
data$gender2[data$gender== 2] <-"여자"
x<- table(data$gender2)
x
prop.table(x) # 비율 계산 : 0< x <1 사이의 값
y <-  prop.table(x)
round(y*100, 2) #백분율 적용(소수점 2자리)


# 3) 나이 변수 리코딩과 비율계산
summary(data$age)# 40 ~ 69
data$age2[data$age <= 45] <-"중년층"
data$age2[data$age >=46 & data$age <=59] <-"장년층"
data$age2[data$age >= 60] <-"노년층"
x<- table(data$age2)
x
prop.table(x) # 비율 계산 : 0< x <1 사이의 값
y <-  prop.table(x)
round(y*100, 2) #백분율 적용(소수점 2자리)

# 4) 학력 수준 변수 리코딩과 비율계산
data$level2[data$level== 1] <-"고졸"
data$level2[data$level== 2] <-"대졸"
data$level2[data$level== 3] <-"대학원졸"

x<- table(data$level2)
x
prop.table(x) # 비율 계산 : 0< x <1 사이의 값
y <-  prop.table(x)
round(y*100, 2) #백분율 적용(소수점 2자리)


# 5) 합격 여부 변수 리코딩과 비율계산
data$pass2[data$pass== 1] <-"합격"
data$pass2[data$pass== 2] <-"실패"
x<- table(data$pass2)
x
prop.table(x) # 비율 계산 : 0< x <1 사이의 값
y <-  prop.table(x)
round(y*100, 2) #백분율 적용(소수점 2자리)
