raw_data2 <- iris
set.seed(100)

#sample()은 무작위 추출함수이며 이를 train_index에 저장하여 train_data를 추출한다
train_index <- sample(1:nrow(raw_data2), size=100, replace=F)
train_data <- raw_data2[train_index,]

#str(train_data)시 100개만 뽑힌 것을 확인할 수 있다
str(train_data)

#원데이터에서 train_data를 빼고 남은 것을 test_data에 넣는 것임
test_data <- raw_data2[-train_index,]
levels(train_data$Species)

#relevel 을 통해 기준열을 잡는다. 이를 하지 않을 시 가장 먼저 잡히는 것을 분석한다. 
#iris의 경우에는 levels()를 통해 확인할 수 있으며, setosa가 먼저 잡힐 것이다.
#이를 기준범주라고 한다.
train_data$Species <- relevel(train_data$Species, "virginica")

library(nnet)
mlogit <- multinom(Species ~., data=train_data)
summary(mlogit)

exp(coef(mlogit))

fit <- fitted(mlogit)
fit

pred <- predict(m, data = test_data, type="response")
pred