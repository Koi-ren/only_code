library(survival)

head(colon)
summary(colon) 

colon_data <- colon
colon_data <- na.omit(colon_data)

summary(colon_data)
str(colon_data)

#관심 예측 변수인 obsturct, perfor, adhere, 
#differ, extent, surg의 자료형이 실수형인 것을 확인
#자료형을 num에서 factor로 변환
colon_data$obstruct <- as.factor(colon_data$obstruct)
colon_data$perfor <- as.factor(colon_data$perfor)
colon_data$adhere <- as.factor(colon_data$adhere)
colon_data$differ <- as.factor(colon_data$differ)
colon_data$extent <- as.factor(colon_data$extent)
colon_data$surg <- as.factor(colon_data$surg)
colon_data$status <- as.factor(colon_data$status)

str(colon_data)
#nodes 제외 모두 factor로 변환완료

set.seed(70)
train_index <- sample(1:nrow(colon_data), size=70, replace=F)
train_data <- colon_data[train_index,]

#str(train_data)시 70개만 뽑힌 것을 확인할 수 있다
str(train_data)

#원데이터에서 train_data를 빼고 남은 것을 test_data에 넣는 것임
test_data <- colon_data[-train_index,]
levels(colon_data$status)

train_data$status <- relevel(train_data$status, "1")

library(nnet)

#반응변수가 이진이기에 glm 사용
m <- glm(status ~ obstruct + perfor + adhere + nodes + extent + surg, 
          data = train_data, family = "binomial"(link = "probit"))

summary(m)

exp(coef(m))

fit <- fitted(m)
fit

#pred <- predict(mlogit, data = test_data, type="probs")
pred <- predict(m, data = test_data, type="response")
pred
