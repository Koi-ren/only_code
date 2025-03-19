# chap17_TimeseriesAnalysis

###############################################
## Chapter17_ 시계열분석(TimeseriesAnalysis)
###############################################

# 시계열(Time-Series) : 관측치 또는 통계량의 변화를 시간의 움직임에 
# 따라서 기록하고, 이것을 계열화한 것을 의미한다.
# 시계열 데이터 : 통계숫자를 시간의 흐름에 따라 일정한 간격마다
# 기록한 통계열을 의미한다.

# 관련분야 : 경기예측, 판매예측, 주식시장분석, 예산분석, 투자연구 등
# 현상 이해 -> 미래 예측

############################
# 시계열 자료 확인
############################

## [실습] 비정상성 시계열 → 정상성 시계열

# 단계 1 : AirPassengers 데이터 셋 가져오기
data(AirPassengers) # 12년간 항공기 탑승 승객 수 
str(AirPassengers) # Time-Series

# 단계 2 : 차분 적용 : 평균 정상화  
par(mfrow=c(1,2))
ts.plot(AirPassengers) # 시계열 시각화
diff <- diff(AirPassengers) # 차분 수행 
plot(diff) # 평균 정상화 

# 단계 3 : 로그 적용 : 분산 정상화  
par(mfrow=c(1,2))
plot(AirPassengers) # 시계열 시각화  
log <- diff(log(AirPassengers)) # 로그+차분 수행 
plot(log) # 분산 정상화 


############################
# 시계열 자료 시각화
############################

## [실습] 단일 시계열 자료 시각화

# 단계 1 : WWWusage 데이터 셋 가져오기
data(WWWusage) # WWWusage   Internet Usage per Minute
str(WWWusage) # Time-Series [1:100] from 1 to 100:
WWWusage

# 단계 2 : 시계열 자료 추세선 시각화
X11()
ts.plot(WWWusage, type="l", col='red')


## [실습] 다중 시계열 자료 시각화

# 단계 1 : 데이터 셋 가져오기
data(EuStockMarkets)
head(EuStockMarkets)
str(EuStockMarkets) # mts [1:1860, 1:4] 2차원 matrix 구조  

# 단계 2 :  데이터프레임으로 변환 
EuStock<- data.frame(EuStockMarkets)
EuStock
head(EuStock)

# 단계 3 : 단일 시계열 데이터 추세선 
X11()
plot(EuStock$DAX[1:1000], type="l", col='red') # 선 그래프 시각화 

# 단계 4 : 다중 시계열 데이터 추세선
plot.ts(cbind(EuStock$DAX[1:1000],EuStock$SMI[1:1000]),main="주가지수 추세선")


############################
# 시계열요소분해 시각화
############################

## [실습] 시계열요소분해 시각화

# 단계 1 : 시계열자료 준비 
data <- c(45, 56, 45, 43, 69, 75, 58, 59, 66, 64, 62, 65, 
          55, 49, 67, 55, 71, 78, 71, 65, 69, 43, 70, 75, 
          56, 56, 65, 55, 82, 85, 75, 77, 77, 69, 79, 89)
length(data)# 36

# 단계 2 : 시계열자료 생성 : 시계열자료 형식으로 객체 생성
tsdata <- ts(data, start=c(2016, 1), frequency=12) 
tsdata # 2016~2018

# 단계 3 : 추세선 확인 
par(mfrow=c(1,1))
ts.plot(tsdata) # plot(tsdata)와 동일함 

# 단계 4 : 시계열 분해
plot(stl(tsdata, "periodic")) # periodic : 주기 

# 단계 5 : 시계열 분해와 변동 요인 제거 
m <- decompose(tsdata) # decompose()함수 이용 시계열 분해
attributes(m) # 변수 보기
plot(m) # 추세요인, 계절요인, 불규칙요인이 포함된 그래프     
plot(tsdata - m$seasonal)  # 계절요인을 제거한 그래프 

#단계 6 : 추세요인과 불규칙요인 제거
plot(tsdata - m$trend) # 추세요인 제거 그래프
plot(tsdata - m$seasonal - m$trend) # 불규칙요인만 출력


#################################
# 자기상관함수/부분자기상관함수 
#################################

## [실습] 시계열요소분해 시각화

# 단계 1 : 시계열자료 생성 
input <- c(3180,3000,3200,3100,3300,3200,3400,3550,3200,3400,3300,3700) 
length(input) # 12
tsdata <- ts(input, start=c(2015, 2), frequency=12) # Time Series
tsdata

# 단계 2 : 자기상관함수 시각화 
acf(na.omit(tsdata), main="자기상관함수", col="red")

# 단계 3 : 부분자기상관함수 시각화
pacf(na.omit(tsdata), main="부분자기상관함수", col="red")


#################################
# 추세 패턴 찾기 시각화 
#################################

## [실습] 시계열 자료의 추세 패턴 찾기 시각화

# 단계 1 :  시계열 자료 생성
input <- c(3180, 3000, 3200, 3100, 3300, 3200, 3400,
              3550, 3200, 3400, 3300, 3700)
# Time Series
tsdata <- ts(input, start=c(2015, 2), frequency=12)

# 단계 2 :  추세선 시각
plot(tsdata, type="l", col='red')

# 단계 3 :  자기 상관 함수 시각화
acf(na.omit(tsdata), main="자기상관함수", col="red")

# 단계 4 : 차분 시각화
plot(diff(tsdata, differences = 1))


############################
# 평활법(Smoothing Method)
############################

## [실습] 이동평균법을 이용한 평활하기

# 단계 1 : 시계열 자료 생성
data <- c(45, 56, 45, 43, 69, 75, 58, 59, 66, 64, 62, 65, 
          55, 49, 67, 55, 71, 78, 71, 65, 69, 43, 70, 75, 
          56, 56, 65, 55, 82, 85, 75, 77, 77, 69, 79, 89)
length(data)# 36
tsdata <- ts(data, start=c(2016, 1), end = c(2018, 10),frequency=12)
tsdata 

# 단계 2 : 평활 관련 패키지 설치
install.packages("TTR")
library(TTR)

# 단계 3 :  이동평균법으로 평활 및 시각화
par(mfrow=c(2, 2))
plot(tsdata, main="원 시계열 자료") # 시계열 자료 시각화
plot(SMA(tsdata, n=1), main="1년 단위 이동평균법으로 평활")
plot(SMA(tsdata, n=2), main="2년 단위 이동평균법으로 평활")
plot(SMA(tsdata, n=3), main="3년 단위 이동평균법으로 평활")


## [실습] 정상성시계열의 비계절형 

# 단계1 : 시계열자료 특성분석 
#(1) 데이터 준비  
input <- c(3180,3000,3200,3100,3300,3200,3400,3550,3200,3400,3300,3700) 

#(2) 시계열객체 생성(12개월 : 2015년 2월 ~ 2016년 1개)
tsdata <- ts(input, start=c(2015, 2), frequency=12) 
tsdata  

#(3) 추세선 시각화
plot(tsdata, type="l", col='red')

# 단계2 : 정상성시계열 변환
par(mfrow=c(1,2))
ts.plot(tsdata)
diff <- diff(tsdata)
plot(diff) # 차분 : 현시점에서 이전시점의 자료를 빼는 연산

# 단계3 : 모형 식별과 추정
install.packages('forecast')
library(forecast)
arima <- auto.arima(tsdata) # 시계열 데이터 이용 
arima

# 단계4 : 모형 생성 
model <- arima(tsdata, order=c(1, 1, 0))
model 

# 단계5 : 모형 진단(모형 타당성 검정)

# (1) 자기상관함수에 의한 모형 진단
tsdiag(model)

# (2) Box-Ljung에 의한 잔차항 모형 진단
Box.test(model$residuals, lag=1, type = "Ljung")

# 단계6 : 미래 예측(업무 적용)
fore <- forecast(model) # 향후 2년 예측
fore
par(mfrow=c(1,2))
plot(fore) # 향후 24개월 예측치 시각화 
model2 <- forecast(model, h=6) # 향후 6개월 예측치 시각화 
plot(model2)


## [실습] 정상성시계열의 계절형

# 단계1 : 시계열자료 특성분석
# (1) 데이터 준비 
data <- c(45, 56, 45, 43, 69, 75, 58, 59, 66, 64, 62, 65, 
          55, 49, 67, 55, 71, 78, 71, 65, 69, 43, 70, 75, 
          56, 56, 65, 55, 82, 85, 75, 77, 77, 69, 79, 89)
length(data)# 36

# (2) 시계열자료 생성 
tsdata <- ts(data, start=c(2016, 1), end = c(2018, 10),frequency=12)
tsdata 
head(tsdata)
tail(tsdata)

# (3) 시계열요소분해 시각화
ts_feature <- stl(tsdata, s.window="periodic")
plot(ts_feature)

# 단계2 : 정상성시계열 변환
par(mfrow=c(1,2))
ts.plot(tsdata)
diff <- diff(tsdata)
plot(diff) # 차분 시각화

# 단계3 : 모형 식별과 추정
library(forecast)
ts_model2 <- auto.arima(tsdata)  
ts_model2

# 단계4 : 모형 생성 
model <- arima(tsdata, c(2, 1, 0), 
               seasonal = list(order = c(1, 0, 0)))
model

# 단계5 : 모형 진단(모형 타당성 검정)
# (1) 자기상관함수에 의한 모형 진단
tsdiag(model)

# (2)Box-Ljung에 의한 잔차항 모형 진단
Box.test(model$residuals, lag=1, type = "Ljung")

# 단계6 : 미래 예측
par(mfrow=c(1,2))
fore <- forecast(model, h=24) # 2년 예측 
plot(fore)
fore2 <- forecast(model, h=6) # 6개월 예측 
plot(fore2)
