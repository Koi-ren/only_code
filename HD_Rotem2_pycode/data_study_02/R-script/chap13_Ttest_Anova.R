# chap13_Ttest_Anova

####################################
##    Chapter13. 집단 간 차이 분석             
####################################

##  1. 추정과 검정
# 추정(estimation) : 표본을 통해서 모집단을 확률적으로 추측   
# 검정통계량 : 표본에 의해서 계산된 통계량(표본평균, 표본표준편차)
# 모수 : 모집단에 의해서 나온 통계량(모평균, 모표준편차)  

# 1) 점 추정 : 제시된 한 개의 값과 검정통계량을 직접 비교하여
#    가설 기각유무를 결정 
# ex) 우리나라 중학교 2학년 남학생 평균키는 165.2cm로 추정

# 2) 구간 추정 : 신뢰구간과 검정통계량을 비교하여 가설 기각유무 결정 
# 신뢰구간 : 오차범위에 의해서 결정된 하한값과 상한값의 범위 
# ex) 우리나라 중학교 2학년 남학생 평균키는 164.5 ~ 165.5cm로 추정


## 2. 단일집단 검정

# 2.1 단일집단 비율검정 

# [실습] 단일표본 빈도수와 비율계산

# 단계 1. 실습데이터 가져오기
setwd("c:/Rwork/Part-III")
data <- read.csv("one_sample.csv", header=TRUE)
head(data)
x <- data$survey


# 단계 2. 빈도수와 비율 계산
summary(x) # 결측치 확인
length(x) # 150개
table(x) # 0:불만족(14), 1: 만족(136) 

# 단계 3. 패키지 이용 빈도수와 비율계산
library(prettyR) # freq() 함수 사용
freq(x) 


# [실습] 만족율 기준 비율검정

# 단계 1. 양측검정
binom.test(c(136, 14), p=0.8) # 기존 80% 만족율 기준 검증 실시
binom.test(c(136, 14), p=0.8, alternative="two.sided", conf.level=0.95)

# 단계 2. 방향성이 갖는 단측가설 검정 
binom.test(c(136, 14), p=0.8, alternative="greater", conf.level=0.95)


# [실습] 불만족율 기준 비율검정

# 단계 1. 양측검정
binom.test(c(14, 136), p=0.2)
binom.test(c(14, 136), p=0.2, alternative="two.sided", conf.level=0.95)

# 단계 2. 방향성이 갖는 단측가설 검정 
binom.test(c(14, 136), p=0.2, alternative="greater", conf.level=0.95)



## 2.2 단일집단 평균검정(단일표본 T검정) 

# (1) 단일표본 평균 계산 

# [실습] 단일표본 평균 계산하기

# 단계 1. 실습파일 가져오기
setwd("c:/Rwork/Part-III")
data <- read.csv("one_sample.csv", header=TRUE)
str(data) # 150
head(data)
x <- data$time
head(x)

# 단계 2. 데이터 분포/결측치 제거
summary(x) # NA-41개
mean(x) # NA

# 단계 3. 데이터 정제 
mean(x, na.rm=T) # NA 제외 평균(방법1)
x1 <- na.omit(x) # NA 제외 평균(방법2)
mean(x1)

# (3) 정규분포 검정
shapiro.test(x1) # 정규분포 검정 함수(p-value = 0.7242) 

# (4) 정규분포 시각화 
hist(x1)
qqnorm(x1)
qqline(x1, lty=1, col= 'blue')

# (5) 평균차이 검정 

# 단계 1. 양측 검정 : x1 객체와 기존 모집단의 평균 5.2시간 비교
t.test(x1, mu=5.2) 
result <- t.test(x1, mu=5.2, alter="two.side", conf.level=0.95) 

# 단계 2. 방향성을 갖는 단측가설 검정
result <- t.test(x1, mu=5.2, alter="greater", conf.level=0.95) 



## 3. 두 집단 검정

# 3.1 두 집단 비율검정 


# (1) 집단별 subset 작성과 교차분석 

# [실습] 두 집단 subset 작성과 교차분석 수행 

# 단계 1. 실습데이터 가져오기
setwd("c:/Rwork/Part-III")
data <- read.csv("two_sample.csv", header=TRUE)
data
head(data) # 변수명 확인

# 단계 2. 두 집단 subset 작성 및 데이터 전처리 
x <- data$method # 교육방법(1, 2) -> 노이즈 없음
y <- data$survey # 만족도(1: 만족, 0:불만족)

# 단계 3. 집단별 빈도분석 
table(x)
table(y)

# 단계 4. 두 변수에 대한 교차분석
table(x, y, useNA="ifany") 


# (2) 두집단 비율차이검증 

# [실습] 두 집단 비율 차이 검정

# 단계 1. 양측 검정
prop.test(c(110,135), c(150, 150)) # 방법1과 방법2 비율차이 검정 
prop.test(c(110,135), c(150, 150), alternative="two.sided", conf.level=0.95)

# 단계 2. 방향성이 있는 단측설 검정  : 방법1 > 방법2 : p-value = 0.9998 > 0.05
prop.test(c(110,135), c(150, 150), alternative="greater", conf.level=0.95)


## 3.2 두 집단 평균검정(독립표본 T검정) 

# (1) 독립표본 평균 계산 

# 단계 1. 실습파일 가져오기
data <- read.csv("c:/Rwork/Part-III/two_sample.csv", header=TRUE)
data 
head(data) #4개 변수 확인
summary(data) # score - NA's : 73개

# 단계 2. 두 집단 subset 작성 및 데이터 전처리
result <- subset(data, !is.na(score), c(method, score))

# 단계 3. 정제된 데이터를 대상으로 subset 생성
result

# 단계 4. 교육방법 별로 분리
a <- subset(result, method==1)
b <- subset(result, method==2)

a1 <- a$score
b1 <- b$score

# 단계 5. 기술통계량 
length(a1); # 109 - a
length(b1); # 118 - b


# (2) 동질성 검정 
var.test(a1, b1) 


# (3) 두 집단 평균 차이 검정 

# 단계 1. 양측검정 
t.test(a1, b1)
t.test(a1, b1, alter="two.sided", conf.int=TRUE, conf.level=0.95)
# p-value = 0.0411 < 0.05 - 두 집단간 평균에 차이가 있다.

# 단계 2. 방향성을 갖는 단측가설 검정 
t.test(a1, b1, alter="greater", conf.int=TRUE, conf.level=0.95)
t.test(a1, b1, alter="less", conf.int=TRUE, conf.level=0.95)


## 3.3 대응 두 집단 평균검정(대응표본 T검정) 

# (1) 대응표본 평균 계산 

# 단계 1. 실습파일 가져오기
setwd("c:/Rwork/Part-III")
data <- read.csv("paired_sample.csv", header=TRUE)
head(data) #  no before after

# 단계 2. 대응 두 집단 subset 생성
result <- subset(data, !is.na(after), c(before,after)) # 100 - 96
x <- result$before
y <- result$after

# 단계 3. 기술통계량 
length(x) # 96
length(y) # 96
mean(x) # 5.145
mean(y, na.rm = T) # 6.220833 -> 1.052  정도 증가


# (2) 동질성 검정  
var.test(x, y, paired=TRUE) 


# (3) 대응 두 집단 평균 차이 검정 

# 단계 1. 양측검정
t.test(x, y, paired=TRUE) # p-value < 2.2e-16 

# 단계 2. 방향성을 갖는 단측가설 검정
t.test(x, y, paired=TRUE,alter="less",conf.int=TRUE, conf.level=0.95) 
# p-value < 2.2e-16 -> x을 기준으로 비교 : x가 y보다 적다.


## 4. 세 집단 검정

# 4.1 세 집단 비율검정 

# (1) 세 집단 subset 작성과 기술 통계량 계산 

# 단계 1. 파일가져오기 
getwd()
setwd("c:/Rwork/Part-III")
data <- read.csv("three_sample.csv", header=TRUE)
data
head(data)

# 단계 2. 세집단 subset 작성(데이터 정제,전처리) 
method <- data$method 
survey<- data$survey
method
survey 

# 단계 3. 기술통계량(빈도분석)
table(method, useNA="ifany") # 50 50 50 -> 3그룹 모두 관찰치 50개
table(method, survey, useNA="ifany") 


# (2) 세 집단 비율 차이 검정 
prop.test(c(34,37,39), c(50,50,50)) # p-value = 0.5232 -> 귀무가설 채택

prop.test(c(34,37,39), c(50,50,50), alternative = 'two.sided',
          conf.level = 0.95) 


## 4.2 분산분석(F 검정) 


# (1) 데이터 전처리 

# 단계 1. 파일 가져오기
data <- read.csv("c:/Rwork/Part-III/three_sample.csv", header=TRUE)

# 단계 2. 데이터 정제/전처리 - NA, outline 제거
data <- subset(data, !is.na(score), c(method, score)) 
data # method, score

# 단계 3. 차트이용 - ontlier 보기(데이터 분포 현황 분석)
plot(data$score) # 차트로 outlier 확인 : 50이상과 음수값
barplot(data$score) # 바 차트
mean(data$score) # 14.45

# 단계 4. outlier 제거 - 평균(14) 이상 제거
length(data$score)
data2 <- subset(data, score <= 14) # 14이상 제거
length(data2$score) 

# 단계 5. 정제된 데이터 보기 
x <- data2$score
boxplot(x)


# (2) 세 집단 subset 작성과 기술 통계량 

# 단계 1. 세 집단 subset 작성
data2$method2[data2$method==1] <- "방법1" 
data2$method2[data2$method==2] <- "방법2"
data2$method2[data2$method==3] <- "방법3"

# 단계 2. 교육방법 별 빈도수
table(data2$method2)  

# 단계 3. 교육방법을 x 변수에 저장
x <- table(data2$method2) 
x

# 단계 4. 교육방법에 따른 시험성적 평균 구하기
y <- tapply(data2$score, data2$method2, mean)
y

# 단계 5. 교육방법과 시험성적으로 데이터프레임 생성
df <- data.frame(교육방법 = x, 성적 = y)
df

# (3) 세 집단 간 동질성 검정 
bartlett.test(score ~ method2, data=data2)


# (4) 분산분석(세 집단 간 평균 차이 검정) 
result <- aov(score ~ method2, data=data2)
names(result)
summary(result) 

