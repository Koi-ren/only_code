data <- read.csv("homework2.csv", header = TRUE, fileEncoding = "cp949")
head(data)
library(PerformanceAnalytics)
#--------전처리---------------------
summary(data)
str(data)
mean(data$중량) # 오류 발생

data$중량[is.na(data$중량)] <- median(data$중량, na.rm = TRUE)
data$연비[is.na(data$연비)] <- median(data$연비, na.rm = TRUE)

#범주형 데이터를 정수형(int)로 받는 문제 발생
data$년식 <- as.factor(data$년식)
data$회사명 <- as.factor(data$회사명)
data$종류 <- as.factor(data$종류)
data$연료 <- as.factor(data$연료)
data$LPG <- as.factor(data$LPG)
data$하이브리드 <- as.factor(data$하이브리드)
data$변속기 <- as.factor(data$변속기)
data$토크 <- as.integer(data$토크)
data$중량 <- as.integer(data$중량)
str(data)

summary(data)
#--------회귀분석---------------------
data_lm <- lm(formula = 가격 ~., data = data)
summary(data_lm)

library(leaps)
all_m <- regsubsets(가격 ~. , data=data)
summary(all_m)
#--------시각화---------------------
sm <- summary(all_m)
sm$bic
sm$adjr2
plot(data_lm)
plot(all_m, scale="adjr2")
plot(data)
