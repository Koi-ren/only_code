# 15_2_Regration

#################################################
## Chapter15_2. 회귀분석(Regression Analysis)
#################################################


## 2.2 단순 회귀분석

# 연구가설 : 제품 적절성은  제품 만족도에 정(正)의 영향을 미친다.
# 연구모델 : 제품적절성(독립변수) -> 제품 만족도(종속변수)

# 단순선형회귀 모델 생성  
# 형식) lm(formula= y ~ x 변수, data) # x:독립, y 종속, data=data.frame

product <- read.csv("C:/Rwork/Part-IV/product.csv", header=TRUE)
str(product) # 'data.frame':  264 obs. of  3 variables:

y = product$제품_만족도 # 종속변수
x = product$제품_적절성 # 독립변수
df <- data.frame(x, y)

# 회귀모델 생성 
result.lm <- lm(formula=y ~ x, data=df)

# (1) 회귀분석의 절편과 기울기 
result.lm # 회귀계수 


# [실습] 모델의 적합값과 잔차 보기 
names(result.lm)
fitted.values(result.lm)[1:2]
head(df, 1) # x=4, y=3
Y = 0.7789 + 0.7393 * 4  
Y # 3.7361

# 오차(잔차:error) = 관측치 - 예측치 
3-3.7361  # -0.7361

residuals(result.lm)[1:2]
-0.7359630 + 3.735963

# [실습] 선형회귀분석 모델 시각화[오류 확인]
# x,y 산점도 그리기 
plot(formula=y ~ x, data=df)
# 회귀분석
result.lm <- lm(formula=y ~ x, data=df)
# 회귀선 
abline(result.lm, col='red')


# [실습] 선형회귀분석 결과 보기
summary(result.lm)


## 2.3 다중 회귀분석 

# - 여러 개의 독립변수 -> 종속변수에 미치는 영향 분석
# 연구가설 : 음료수 제품의 적절성(x1)과 친밀도(x2)는 제품 만족도(y)에 정의 영향을 미친다.
# 연구모델 : 제품 적절성(x1), 제품 친밀도(x2) -> 제품 만족도(y)

product <- read.csv("C:/Rwork/Part-IV/product.csv", header=TRUE)

#(1) 적절성 + 친밀도 -> 만족도  
y = product$제품_만족도 # 종속변수
x1 = product$제품_친밀도 # 독립변수2
x2 = product$제품_적절성 # 독립변수1
df <- data.frame(x1, x2, y)

result.lm <- lm(formula=y ~ x1 + x2, data=df)

# 계수 확인 
result.lm
# 0.66731(y절편)      0.09593(x1)  0.68522(x2)      


# 분산팽창요인 
install.packages("car") # vif() 함수 제공 패키지 설치
library(car) # 메모리 로딩

#단계 2 : 분산팽창요인(VIF)
vif(result.lm) 
sqrt(vif(result.lm) ) > 2 # FALSE FALSE 


## 2.4 다중공선성 문제 해결과 모델 성능평가


# [실습] 다중공선성 문제 확인

# (1) 패키지 설치 및 데이터 로딩 
install.packages("car")
library(car)
data(iris)

# (2) iris 데이터 셋으로 다중회귀분석
fit <- lm(formula=Sepal.Length ~ Sepal.Width+Petal.Length+Petal.Width, data=iris)
vif(fit)
sqrt(vif(fit))>2 # root(VIF)가 2 이상인 것은 다중공선성 문제 의심 

# (3) iris 변수 간의 상관계수 구하기
cor(iris[,-5]) # 변수간의 상관계수 보기(Species 제외) 
#x변수 들끼 계수값이 높을 수도 있다. -> 해당 변수 제거(모형 수정) <- Petal.Width

# [실습] 데이터 셋 생성과 회귀모델 생성

# (1) 학습데이터와 검정데이터 분류
x <- sample(1:nrow(iris), 0.7*nrow(iris)) # 전체중 70%만 추출
train <- iris[x, ] # 학습데이터 추출
test <- iris[-x, ] # 검정데이터 추출

# (2) 변수 제거 및 다중회귀분석 - Petal.Width 변수를 제거한 후 회귀분석 
# - 학습데이터 이용 모델 생성 
model <- lm(formula=Sepal.Length ~ Sepal.Width + Petal.Length, data=train)

# (3) 회귀방정식 도출 
model 
head(train, 1)
Y = 2.0873 + 0.6369 * 3.6 + 0.4785 * 6.1
Y

# (4) 예측치 생성 - predict()함수
# - 회귀분석 결과를 대상으로 회귀방정식을 적용한 새로운 값 예측(Y값)
pred <- predict(result.lm, test)# x변수만 test에서 찾아서 값 예측
pred # test 데이터 셋의 y 예측치(회귀방정식 적용) 
test$Sepal.Length # test 데이터 셋의 y 관측치  
length(pred) # 45개 벡터

# (5) 회귀모델 평가 
cor(pred, test$Sepal.Length)
summary(pred); summary(test$Sepal.Length)



##  2.5 기본가정 충족으로 회귀분석 수행

# [실습] 기본가정 충족으로 회귀분석 수행 

# 1. 회귀모델 생성 
# (1) 변수 모델링 : y:Sepal.Length <- x:Sepal.Width,Petal.Length,Petal.Width
formula = Sepal.Length ~ Sepal.Width + Petal.Length + Petal.Width

# (2) 회귀모델 생성 
model <- lm(formula = formula,  data=iris)
model


# 2. 잔차[오차] 분석

# (1) 독립성과 등분산성 검정  
#install.packages('lmtest')
library(lmtest) # 자기상관 진단 패키지 설치 
dwtest(model) # 더빈 왓슨 값(통상 1~3 사이)

# 등분산성 검정 
plot(model, which =  1) 
methods('plot') # plot()에서 제공되는 객체 보기 

# (2) 잔차 정규성 검정
attributes(model) # coefficients(계수), residuals(잔차), fitted.values(적합값)
res <- residuals(model) # 잔차 추출 
shapiro.test(res) # 정규성 검정 - p-value = 0.9349 >= 0.05
# 귀무가설 : 정규성과 차이가 없다.

# 정규성 시각화  
hist(res, freq = F) 
qqnorm(res)


# 3. 다중공선성 검사 
library(car)
sqrt(vif(model)) > 2 # TRUE 

# 4. 회귀모델 생성/평가 
formula = Sepal.Length ~ Sepal.Width + Petal.Length 
model <- lm(formula = formula,  data=iris)
summary(model) # 모델 평가