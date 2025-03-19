#chap06_DataHandling

#####################################
## Chapter06. 데이터 조작 
#####################################

## 1. plyr 패키지 활용 

# 1.1 데이터 병합 

# [실습] 데이터 병합하기 
install.packages('plyr')
library(plyr) # 패키지 로딩

# 병합할 데이터프레임 셋 만들기
x = data.frame(id = c(1,2,3,4,5), height = c(160,171,173,162,165))
y = data.frame(id = c(5,4,1,3,2), weight = c(55,73,60,57,80))

z <- join(x, y, by='id') # ID컬럼으로 조인
z

# [실습]  왼쪽(Left) 조인하기 
x = data.frame(id = c(1,2,3,4,6), height = c(160,171,173,162,180))
y = data.frame(id = c(5,4,1,3,2), weight = c(55,73,60,57,80))
left <- join(x, y, by='id') # ID컬럼으로 left 조인(왼쪽 변수 기준)
left

# [실습] 내부(Inner)조인하기 
x = data.frame(id = c(1,2,3,4,5), height = c(160,171,173,162,165))
y = data.frame(id = c(5,4,1,3,2), weight = c(55,73,60,57,80))
inner <- join(x, y,by='id', type='inner') # type='inner' : 값이 있는 것만 조인
inner

# [실습] 전체(Full)조인하기 
x = data.frame(id = c(1,2,3,4,6), height = c(160,171,173,162,180))
y = data.frame(id = c(5,4,1,3,2), weight = c(55,73,60,57,80))
full <- join(x,y,by='id', type='full') # type='full' : 모든 항목 조인
full

# [실습] key값으로 병합하기
x = data.frame(key1 = c(1,1,2,2,3),  key2 = c('a','b','c','d','e'),
               val1 = c(10,20,30,40,50))
y = data.frame(key1 = c(3,2,2,1,1),  key2 = c('e','d','c','b','a'),
               val2 = c(500,400,300,200,100))

join(x, y, by=c('key1', 'key2'))


# 1.2 그룹별 기술 통계량 구하기  

# (1) tapply() 함수 이용 

# [실습] iris 데이터 셋을 대상으로 tapply() 함수 적용하기
head(iris)
names(iris)
unique(iris$Species)

tapply(iris$Sepal.Length, iris$Species, mean)
tapply(iris$Sepal.Length, iris$Species, sd)


# (2) ddply() 함수 이용

# [실습] 꽃의 종류별(Species)로 꽃받침 길이의 평균 구하기
avg_df <- ddply(iris, .(Species), summarise, avg = mean(Sepal.Length))
avg_df
str(avg_df)


# [실습] 꽃의 종(Species)로 여러 개의 함수 적용하기 
a <- ddply(iris, .(Species), summarise, 
            avg = mean(Sepal.Length),
            std = sd(Sepal.Length),
            max = max(Sepal.Length),
            min = min(Sepal.Length))

# [실습]  round() 함수를 적용하여 avg, std 칼럼에 반올림 처리하기 
b <- ddply(iris, .(Species), summarise, 
           avg = round(mean(Sepal.Length), 2),
           std = round(sd(Sepal.Length), 2),
           max = max(Sepal.Length), min = min(Sepal.Length))


## 2. dplyr 패키지 활용

# 2.1 콘솔 창의 크기에 맞게 데이터 추출 

# [실습] dplyr 패키지와 데이터 셋 hflight 설치
install.packages(c("dplyr", "hflights"))
library(dplyr)
library(hflights) 
str(hflights)

# [실습]  콘솔 창 안에서 한 눈으로 파악하기 
hflights_df <- tbl_df(hflights)
hflights_df


# 2.2 조건에 맞는 데이터 필터링

# [실습] hflights_df를 대상으로 1월 2일 데이터 추출하기
filter(hflights_df, Month == 1 & DayofMonth == 2) # AND(&)

# [실습] 1월 혹은 2월 데이터 추출
filter(hflights_df, Month == 1 | Month == 2) # OR


# 2.3 칼럼으로 데이터 정렬 

# [실습] 년, 월, 출발시간, 도착시간 순으로 오름차순 정렬
arrange(hflights_df, Year, DepTime, ArrTime )

# [실습] 출발시간으로 내림차순 정렬하기 
arrange(hflights_df, Year, Month, desc(DepTime), ArrTime)


# 2.4 칼럼으로 데이터 검색 

# [실습] hflights_df에서 년, 월, 출발시간, 도착시간 칼럼 검색하기
select(hflights_df, Year, Month, DepTime, ArrTime)  # 4개 칼럼 선택

# [실습] 칼럼의 범위 지정하기 
select(hflights_df, Year:ArrTime)

# 칼럼의 범위 제외 : Year부터 DayOfWeek 제외
select(hflights_df, -(Year:DayOfWeek))


# 2.5 데이터 셋에 칼럼 추가 

# [실습] 출발지연시간과 도착지연시간과의 차이를 계산하는 칼럼 추가하기
mutate(hflights_df, gain = ArrDelay - DepDelay, 
       gain_per_hour = gain/(AirTime/60) )


# [실습] mutate() 함수에 의해서 추가된 칼럼 보기
select(mutate(hflights_df, gain = ArrDelay - DepDelay, 
              gain_per_hour = gain/(AirTime/60) ), 
       Year, Month, ArrDelay, DepDelay, gain, gain_per_hour)


# 2.6 요약 통계치 계산 

# [실습] 비행시간 평균 계산하기
summarise(hflights_df, avgAirTime = mean(AirTime, na.rm = TRUE))

# [실습] 데이터 셋의 관측치 길이 구하기
summarise(hflights_df, cnt = n(), delay = mean(DepDelay, na.rm = TRUE))


# [실습] 도착시간(ArrTime)의 표준편차와 분산 계산하기
summarise(hflights_df, arrTimeSd = sd(AirTime, na.rm = TRUE),
              arrTimeVar = var(AirTime, na.rm = T))

# 2.7  집단변수 대상 그룹화 

# [실습] 집단변수를 이용하여 그룹화하기
species <- group_by(iris, Species)
str(species)


## 3. reshape 패키지 활용

# 3.1 칼럼명 변경 

#단계 1 : 패키지 설치
install.packages("reshape") 
library(reshape)

#단계 2 : 실습 데이터 셋 가져오기
result <- read.csv("C:/Rwork/Part-II/reshape.csv", header=FALSE) 
head(result) 

#단계 3 : 칼럼명 변경
result <- rename(result, c(V1="total", V2="num1", V3="num2", V4="num3")) 
head(result) # total num1 num2 num3


# 3.2 긴 형식을 넓은 형식으로 변경 
data('Indometh') # Indometh 기본 데이터 셋 확인
str(Indometh) 

Indometh # 긴 형식 보기
range(Indometh$Subject)
# 긴 형식 -> 넓은 형식 
wide <- reshape(Indometh, 
                v.names = "conc",
                timevar = "time", idvar = "Subject",
                direction = "wide")
wide

# [실습] 넓은 형식을 긴 형식으로 변경 
reshape(wide, direction = "long")



## 4. reshape2 패키지 활용

# 4.1 긴 형식을 넓은 형식으로 변경 

# [실습] 패키지 설치와 데이터 가져오기
install.packages('reshape2')
library(reshape2)

# [실습] 데이터 가져오기 
data <- read.csv("C:\\Rwork\\Part-II\\data.csv")
data

# [실습]  '넓은 형식'(wide format)으로 변경
wide <- dcast(data, Customer_ID ~ Date, sum)
wide 

# [실습] 파일 저장 및 읽기  
setwd("c:/Rwork/Part-II")
write.csv(wide, 'wide.csv', row.names=FALSE) # 행 번호 없음

wide <- read.csv('wide.csv')
colnames(wide) <- c('Customer_ID','day1','day2','day3','day4','day5','day6','day7')
wide


# 4.2 넓은 형식을 긴 형식으로 변경 

# [실습] melt() 함수 이용 : ‘넓은 형식’을 ‘긴 형식’으로 변경하기
long <- melt(wide, id='Customer_ID') 
long

# 칼럼명 수정
name <- c("Customer_ID", "Date", "Buy")
colnames(long) <- name   
head(long)

# [실습]  reshape2 패키지의 smiths 데이터 셋 구조 변경하기 
data("smiths")
smiths

# wide -> long 
long <- melt(id=1:2, smiths)
long

# long -> wide 
dcast(long, subject + time ~...)


# 4.3 3차원 배열 형식으로 변경 

# [실습]  airquality 데이터 셋 구조변경
data('airquality') # airquality  New York Air Quality Measurements
airquality
str(airquality) # data.frame':	153 obs. of  6 variables:

# 칼럼명 대문자 일괄 변경
names(airquality) <- toupper(names(airquality)) # 칼럼명 대문자 변경
head(airquality)

# 월과 일 칼럼으로 나머지 4개 칼럼을 묶어서 긴 형식 변경 
air_melt <- melt(airquality, id=c("MONTH", "DAY"), na.rm=TRUE)
head(air_melt) # month day variable value

# 일과 월 칼럼으로 variable 칼럼을 3차원 형식으로 분류   
names(air_melt) <- tolower(names(air_melt)) # 칼럼명 소문자 변경
acast<- acast(air_melt, day ~ month ~ variable)
acast

# 월 단위 variable(대기관련 칼럼) 칼럼 합계
acast(air_melt, month ~ variable, sum, margins = TRUE)  
