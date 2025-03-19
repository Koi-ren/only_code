# chap15_4_1_DecisionTree

#############################################
## Chapter15_4_1. 분류분석(Decision Tree)
#############################################
# - 종속변수(y변수) 존재
# - 종속변수 : 예측에 Focus을 두는 변수
# - 비모수 검정 : 선형성, 정규성, 등분산성 가정 필요없음
# - 단점 : 유의수준 판단 기준 없음(추론 기능 없음)
# - 규칙(Rule)을 기반으로 의사결정트리 생성


## 1. party 패키지 적용 분류분석

## [실습1] ctree  함수 이용 의사결정트리 생성하기

# 단계1 : part패키지 설치
install.packages("party")
library(party) # ctree() 제공

# 단계2 : airquality 데이터 셋 로딩
library(datasets)
str(airquality)

# 단계3 : formula 생성
formula <-  Temp ~ Solar.R +  Wind + Ozone

# 단계4 : 분류모델 생성 : formula를 이용하여 분류모델 생성 
air_ctree <- ctree(formula, data=airquality)
air_ctree

# 단계5  : 분류분석 결과
plot(air_ctree)

# 분류조건 subset 작성/확인 
result <- subset(airquality, Ozone <= 37 & Wind > 15.5)
summary(result$Temp)


## [실습2] 학습데이터와 검정데이터 샘플링으로 분류분석하기 

#단계1 : 학습데이터와 검증데이터 샘플링
#set.seed(1234) # 메모리에 시드값 적용 - 동일값 생성 
idx <- sample(1:nrow(iris), nrow(iris) * 0.7) 
train <- iris[idx,] 
test <- iris[-idx,]  

# 단계2 : formula 생성 
#  -> 형식) 변수 <- 종속변수 ~ 독립변수
formula <- Species ~ Sepal.Length+Sepal.Width+Petal.Length+Petal.Width 

#단계3 : 학습데이터 이용 분류모델 생성(ctree()함수 이용)
iris_ctree <- ctree(formula, data=train) # 학습데이터로 분류모델(tree) 생성
iris_ctree # Petal.Length,Petal.Width 중요변수

#단계4 : 분류모델 플로팅
# plot() 이용 - 의사결정 트리로 결과 플로팅
plot(iris_ctree, type="simple") 
plot(iris_ctree) # 의사결정트리 해석

result <- subset(train, Petal.Length > 1.9 & Petal.Width <= 1.7 & Petal.Length > 4.6)
result$Species
length(result$Species) # 9
table(result$Species)
#setosa versicolor  virginica 
#     0          5          4 

#단계5 : 분류모델 평가 

# (1) 모델 예측치 생성과 혼돈 매트릭스 생성 
pred <- predict(iris_ctree, test) # 45
pred # Y변수의 변수값으로 예측 

table(pred, test$Species)
#pred         setosa versicolor virginica
#setosa         14          0         0   <- missing : 0
#versicolor      0         15         0   <- missing : 0
#virginica       0          1        15   <- missing : 1

# (2) 분류정확도 
(14+15+15) / nrow(test) # 0.9777778


## [실습3] K겹 교차검정 샘플링으로 분류분석하기 
# - iris 데이터 셋을 대상으로 K=3, R=2 교차검정 샘플링 방법으로 분류분석 

#단계1: K겹 교차검정을 위한 샘플링 
library(cvTools)
cross <- cvFolds(nrow(iris), K=3, R=2) 

#단계2: K겹 교차검정 데이터 보기
str(cross) # 구조 보기 

cross # 5겹 교차검정 데이터 보기
length(cross$which) # 150
dim(cross$subsets) # 150   2

#단계3: K겹 교차검정 수행  
R=1:2 # 2회 반복  
K=1:3 # 3겹  
CNT = 0 # index
ACC <- numeric()  # 분류정확도 vector
for(r in R){ # 2회 
  cat('\n R=',r, '\n')  
  for(k in K){ # 3회 
    # test 생성 
    datas_idx <- cross$subsets[cross$which==k, r] 
    test <- iris[datas_idx, ] # 검정데이터 생성
    cat('test : ', nrow(test), '\n')
    # train 생성 
    formula <- Species ~ .    
    train <- iris[-datas_idx, ]   # 훈련데이터 생성 
    cat('train : ', nrow(train), '\n')  
    # model 생성 
    model <- ctree(formula, data=train)
    pred <- predict(model, test)
    t <- table(pred, test$Species)
    print(t)
    CNT <- CNT + 1
    ACC[CNT] <- (t[1,1]+t[2,2]+t[3,3]) / sum(t) 
  }    
} 
CNT # K겹 교차검정 회전수

#단계4: 교차검정 모델 평가  
ACC 
length(ACC)

mean(ACC, na.rm = T) # 산술평균


## [실습4] 고속도록 주행 거리에 미치는 영향변수 보기 

#단계1: 패키지 설치 및 로딩
library(ggplot2) 
data(mpg) # ggplot2 패키지 제공

#단계2: 학습데이터와 검정데이터 생성
t <- sample(1:nrow(mpg), 120) 
train <- mpg[t, ] 
test <- mpg[-t, ]   
dim(test)

#단계3: formula 작성과 분류모델 생성
test$drv <- factor(test$drv)
formula <- hwy ~ displ + cyl + drv
hwy_ctree <- ctree(formula, data=test) 
plot(hwy_ctree) 

## [실습5] AdultUCI 데이터 셋을 이용한 분류분석

# 단계1 : 패키지 설치 및 데이터 셋 구조 보기 
library(arules)
data("AdultUCI")

str(AdultUCI) # 'data.frame':	48842 obs. of  15 variables:
names(AdultUCI)

# 단계2 : 데이터 샘플링 - 10,000개 관측치 선택 
set.seed(1234) # 메모리에 시드 값 적용
choice <- sample(1:nrow(AdultUCI), 10000)
choice
adult.df <-  AdultUCI[choice, ]  
str(adult.df) # ' # 'data.frame':	10000 obs. of  15 variables:

# 단계3 : 변수 추출 및 데이터 프레임 생성
# (1) 변수 추출
capital<- adult.df$`capital-gain`
hours<- adult.df$`hours-per-week`
education <- adult.df$`education-num`
race <- adult.df$race
age <- adult.df$age
income <- adult.df$income

# (2) 데이터프레임 생성
adult_df <- data.frame(capital=capital, age=age, race=race, hours=hours, education=education, income=income)
str(adult_df) # 'data.frame':	10000 obs. of  6 variables:

# 단계4 : formula 생성 - 자본이득(capital)에 영향을 미치는 변수 
formula <-  capital ~ income + education + hours + race + age

# 단계5 :  분류모델 생성 및 예측
adult_ctree <- ctree(formula, data=adult_df)
adult_ctree # 가장 큰 영향을 미치는 변수 - income, education

# 단계6 : 분류모델 플로팅
plot(adult_ctree)


## 2. rpart 패키지 적용 분류분석

## [실습1] rpart()함수 간단 실습 

# 단계1 : 패키지 설치 및 로딩 
install.packages("rpart")
library(rpart)
install.packages("rpart.plot")
library(rpart.plot)
install.packages('rattle')
library('rattle')

# 단계2 : 데이터 로딩
data(iris)
X11() # 별도창 

# 단계3 : rpart() 함수 이용 분류분석
iris.df <- rpart(Species ~ ., data=iris)
iris.df  

# 단계4 : 분류분석 시각화
plot(iris.df ) # 트리 프레임 보임
text(iris.df, use.n=T, cex=0.6) # 텍스트 추가
post(iris.df, file="")


## [실습2] 날씨 데이터를 이용하여 비 유무 예측 
#  weather.csv를 weather로 읽어서 RainTomorrow가 y변수, Date, RainTody를
#  제외한 나머지 변수가 x변수가 되도록 하여 decision tree를 작성

# 단계1 : 데이터 가져오기
# c:/Rwork/Part-IV/weather.csv 파일 선택
weather = read.csv("c:/Rwork/Part-IV/weather.csv", header=TRUE) 

# 단계2 : 데이터 특성 보기
str(weather) # data.frame':  366 obs. of  15 variables:
names(weather) # 15개 변수명
head(weather)

# 단계3 : 분류분석 - 의사결정트리 생성
weather.df <- rpart(RainTomorrow ~ ., 
                    data=weather[, c(-1,-14)], cp=0.01)
weather.df

# 단계4 : 분류분석 시각화
X11()
plot(weather.df) # 트리 프레임 보임
text(weather.df, use.n=T, cex=0.7) # 텍스트 추가
post(weather.df, file="") # 타원제공 - rpart 패키지 제공 

rpart.plot(weather.df)

## 단계5 : 예측치 생성과 코딩 변경
weather_pred <- predict(weather.df, weather)
weather_pred

# y의 범주로 코딩 변환 : Yes(0.5이상), No(0.5 미만)
weather_pred2 <- ifelse(weather_pred[,2] >= 0.5, 'Yes', 'No' )

# 단계6 : 모델 평가(분류 정확도) 
table(weather_pred2, weather$RainTomorrow)
(278+53) / nrow(weather) # 0.9043716





