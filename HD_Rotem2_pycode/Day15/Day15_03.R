# H0 : 교육방법에 따른 세집단 간 실기시험의 평균에 차이가 없다
# H1 : 교육방법에 따른 세집단 간 실기시험의 평균에 차이가 있다

data <- read.csv("three_sample.csv", header=TRUE)
head(data) 

data <- subset(data, !is.na(score), c(method, score)) 
head(data) # method, score

plot(data$score) # 산점도 이용 outlier 확인(50이상 발견)
barplot(data$score) # 막대 차트 이용 outlier 확인
mean(data$score) # 평균 통계량 : 14.442

length(data$score) # outlier 제거 전 관측치 91개
data2 <- subset(data, score <= 14) # 14이상 제거
length(data2$score) #88 (3개 제거)

x <- data2$score
boxplot(x) # 박스 차트에서 정제 데이터 확인  

data2$method2[data2$method==1] <- "방법1" 
data2$method2[data2$method==2] <- "방법2"
data2$method2[data2$method==3] <- "방법3"

table(data2$method2)
x <- table(data2$method2)
#사례의 수가 기계 학습에 굉장히 중요한 역할을 한다 학습 사례가 많을수록  

y <- tapply(data2$score, data2$method2, mean)
y

df <- data.frame(교육방법=x, 성적=y) 
df # 교육방법에 따른 시험성적 평균 교차표 

bartlett.test(score ~ method, data=data2)

help(aov) # 형식) aov(종속변수 ~ 독립변수, data=data set)
result <- aov(score ~ method2, data=data2)
names(result) 

summary(result) 

TukeyHSD(result) # 분산분석의 결과로 사후검정 
#두개씩 묶어서 서로간의 사후검정을 진행하는 함수

plot(TukeyHSD(result))
