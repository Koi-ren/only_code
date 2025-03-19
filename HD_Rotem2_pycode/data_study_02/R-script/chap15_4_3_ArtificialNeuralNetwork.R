# chap15_4_3_ArtificialNeuralNetwork

############################################
## Chapter15_4_3. ArtificialNeuralNetwork
############################################

## [실습1] 간단한 인공신경망 모델 생성  

# 단계1 : 패키지 설치
install.packages("nnet")   # 인공신경망 모델 생성 패키지 
library(nnet)

# 단계2 :  데이터 셋 생성 
 df = data.frame(
          x2 = c(1:6),
          x1 = c(6:1),
          y = factor( c('no', 'no', 'no', 'yes', 'yes', 'yes'))  
 )
str(df)

# 단계3 : 인공신경망 모델 생성 
model_net = nnet(y ~ ., df, size = 1) # size는 분석자가 지정

# 단계4 : 모델 결과변수 보기
model_net

# 단계5 : 가중치 보기
summary(model_net)

# 단계6 :  분류모델 적합값 보기
model_net$fitted.values # 변수 이용(비율 예측) 

# 단계7 : 분류모델의 예측치 생성과 분류 정확도
p <- predict(model_net, df, type="class") # 범주 예측 
table(p, df$y)  # 분류정확도


## [실습2] iris 데이터 셋을 이용한 인공신경망 모델 생성

# 단계1 : 데이터 셋 생성  
data(iris)
idx = sample(1:nrow(iris), 0.7*nrow(iris))
training = iris[idx, ]
testing = iris[-idx, ]
nrow(training) # 105(70%)
nrow(testing) # 45(30%)

# 단계2 :  인공신경명 모델 생성 
model_net_iris1 = nnet(Species ~ ., training, size = 1) # hidden=1
model_net_iris1 # 11 weights

model_net_iris3 = nnet(Species ~ ., training, size = 3) # hidden=3 
model_net_iris3 # 27 weights

# 단계3 : 가중치 망보기  
summary(model_net_iris1) # 11개 가중치 확인
summary(model_net_iris3) # 27개 가중치 확인 


# 단계4 : 분류모델 평가 
table(predict(model_net_iris1, testing, type = "class"), testing$Species)
table(predict(model_net_iris3, testing, type = "class"), testing$Species)


## [실습3]  neuralnet 패키지 이용 인공신경망 모델 생성

# 단계1 : 패키지 설치
install.packages('neuralnet')
library(neuralnet)

# 단계2 : 데이터 셋 생성 
data("iris")
idx = sample(1:nrow(iris), 0.7*nrow(iris))
training_iris = iris[idx, ]
testing_iris = iris[-idx, ]
dim(training_iris) # 105   6
dim(testing_iris) # 45  6

# 단계3 : 숫자형으로 칼럼 생성 
training_iris$Species2[training_iris$Species == 'setosa'] <- 1
training_iris$Species2[training_iris$Species == 'versicolor'] <- 2
training_iris$Species2[training_iris$Species == 'virginica'] <- 3
training_iris$Species <- NULL
head(training_iris)

testing_iris$Species2[testing_iris$Species == 'setosa'] <- 1
testing_iris$Species2[testing_iris$Species == 'versicolor'] <- 2
testing_iris$Species2[testing_iris$Species == 'virginica'] <- 3
testing_iris$Species <- NULL
head(testing_iris)

# 단계4 : 데이터 정규화 
# (1) 정규화 함수 정의 : 0 ~ 1 범위로 정규화 
normal <- function(x){
  return (( x - min(x)) / (max(x) - min(x)))
}

# (2) 정규화 함수를 이용하여 학습데이터/검정데이터 정규화 
training_nor <- as.data.frame(lapply(training_iris, normal))
summary(training_nor) # 0 ~ 1 확인

testing_nor <- as.data.frame(lapply(testing_iris, normal))
summary(testing_nor) # 0 ~ 1 확인

# 단계5 : 인공신경망 모델 생성 : 은닉노드 1개
model_net = neuralnet(Species2 ~ Sepal.Length+Sepal.Width+Petal.Length+Petal.Width, 
                      data=training_nor, hidden = 1)
model_net

plot(model_net) # Neural Network 모형 시각화 

# 단계6 : 분류모델 성능 평가
# (1) compute() 함수 이용 
model_result <- compute(model_net, testing_nor[c(1:4)])
model_result$net.result # 분류 예측값 보기  

# (2) 상관분석 : 상관계수로 두 변수 간의 선형관계의 강도 측정 
cor(model_result$net.result, testing_nor$Species2)

# 단계7 : 분류모델 성능 향상 : 은닉노드 2개, backprop 적용 
# (1) 인공신경망 모델 생성 
model_net2 = neuralnet(Species2 ~ Sepal.Length+Sepal.Width+Petal.Length+Petal.Width, 
                       data=training_nor, hidden = 2, algorithm="backprop", learningrate=0.01 ) 

# (2) 분류모델 예측치 생성과 평가 
model_result2 <- compute(model_net2, testing_nor[c(1:4)])
cor(model_result2$net.result, testing_nor$Species2)  

