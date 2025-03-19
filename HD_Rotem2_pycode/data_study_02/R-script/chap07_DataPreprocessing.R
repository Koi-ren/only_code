# chap07_DataPreprocessing

#####################################
## Chapter07. 데이터 전처리 
#####################################

# 1. 탐색적 데이터 조회 

# 1.1 데이터 셋 보기 

# [실습] 데이터 가져오기 
setwd("C:/Rwork/Part-II")
dataset <- read.csv("dataset.csv", header=TRUE) # 헤더가 있는 경우
# dataset.csv - 칼럼과 척도 관계 

# 1) 데이터 조회
# - 탐색적 데이터 분석을 위한 데이터 조회 

# [실습] 전체 데이터 보기 
print(dataset)
View(dataset) # 뷰어창 출력

# [실습]  데이터의 앞부분과 뒷부분 보기  
head(dataset) 
tail(dataset) 

# 1.2 데이터 셋 구조 보기 

# [실습] 데이터 셋 구조
names(dataset) # 변수명(컬럼)
attributes(dataset) 
str(dataset) # 데이터 구조보기

# 1.3 데이터 셋 조회

# [실습] 데이터 셋 조회   
dataset$age 
dataset$resident
length(dataset$age) # data 수-300개 

# 조회결과 변수 저장
x <- dataset$gender 
y <- dataset$price

# 산점도 형태로 변수 조회 
plot(x, y) # 성별과 가격분포 - 극단치 발견 

#산점도 형태로 변수 조회
plot(dataset$price)

# [실습] [“칼럼명”] 형식으로 특정 변수 조회
dataset["gender"] # dataset$gender
dataset["price"]

# [실습] [색인(index)] 형식으로 변수 조회
dataset[2] # 두번째 컬럼
dataset[6] # 여섯번째 컬럼
dataset[3,] # 3번째 관찰치(행) 전체
dataset[,3] # 3번째 변수(열) 전체

# [실습] [색인(index)] 형식으로 변수 조회
dataset[c("job","price")]
dataset[c(2,6)] 

dataset[c(1,2,3)] 
dataset[c(1:3)] 
dataset[c(2,4:6,3,1)] 
dataset[-c(2)] # dataset[c(1,3:7)] 

# [실습] dataset의 특정 행/열을 조회하는 경우
dataset[, c(2:4)]     
dataset[c(2:4), ]
dataset[-c(1:100), ]   


# 2. 결측치(NA) 처리

# 2.1 결측치 확인 

# [실습]  summary() 함수 이용 
summary(dataset$price) 
sum(dataset$price) # NA 출력


# 2.2 결측치 제거 

# [실습] sum() 함수에서 제공되는 속성 이용  
sum(dataset$price, na.rm=T) 

# [실습] 결측데이터 제거 함수 이용  
price2 <- na.omit(dataset$price) 
sum(price2) 
length(price2) # 30개 제거


# 2.3 결측치 대체 

# [실습] 결측를 으로 대체하기
x <- dataset$price # price vector 생성 
x[1:30]
dataset$price2 = ifelse( !is.na(x), x, 0) # 0으로 대체
dataset$price2[1:30]

# [실습] 결측데이터 처리(평균으로 대체)
x <- dataset$price # price vector 생성 
x[1:30] # 5.1 4.2 4.7 3.5 5.0
dataset$price3 = ifelse(!is.na(x), x, round(mean(x, na.rm=TRUE), 2) ) # 평균으로 대체
dataset$price3[1:30]
dataset[c('price', 'price2', 'price3')]


# 3. 극단치 처리 

# 3.1 범주형 변수 극단치 처리

# [실습] 범주형 변수의 극단치 확인 
table(dataset$gender) # 빈도수
pie(table(gender)) # 파이 차트

# [실습] subset() 함수를 이용한 데이터 정제하기 
dataset <- subset(dataset, gender==1 | gender==2)
dataset # gender변수 데이터 정제
length(dataset$gender) # 297개 - 3개 정제됨
pie(table(dataset$gender))
pie(table(dataset$gender), col = c('red', 'blue'))


# 3.2  연속형 변수의 극단치 처리 
dataset <- read.csv('dataset.csv', header = T)
dataset$price # 세부데이터 보기
length(dataset$price) #300개(NA포함)
plot(dataset$price) # 산점도 
summary(dataset$price) # 범위확인


# [실습] price변수의 데이터 정제와 시각화 
dataset2 <- subset(dataset, price >= 2 & price <= 8)
length(dataset2$price) 
stem(dataset2$price) # 줄기와 잎 도표보기

# [실습] age 변수에서 NA 발견
summary(dataset2$age)
length(dataset2$age) 
dataset2 <- subset(dataset2, age >= 20 & age <= 69)
length(dataset2$age) 
boxplot(dataset2$age) 


# 4. 코딩변경 

# 4.1 가독성을 위한 코딩변경 

# [실습] 가독성을 위한 코딩 변경   
dataset2$resident2[dataset2$resident == 1] <-'1.서울특별시'
dataset2$resident2[dataset2$resident == 2] <-'2.인천광역시'
dataset2$resident2[dataset2$resident == 3] <-'3.대전광역시'
dataset2$resident2[dataset2$resident == 4] <-'4.대구광역시'
dataset2$resident2[dataset2$resident == 5] <-'5.시구군'
dataset2[c("resident","resident2")] # 2개만 지정

# [실습] job 칼럼을 대상으로 코딩 변경하기
dataset2$job2[dataset2$job == 1] <- '공무원'
dataset2$job2[dataset2$job == 2] <- '회사원'
dataset2$job2[dataset2$job == 3] <- '개인사업'


# 4.2 척도 변경을 위한 코딩 변경 

# [실습] 나이(age) 변수를 청년층, 중년층, 장년층으로 코딩 변경하기 
dataset2$age2[dataset2$age <= 30] <-"청년층"
dataset2$age2[dataset2$age > 30 & dataset2$age <=55] <-"중년층"
dataset2$age2[dataset2$age > 55] <-"장년층"
head(dataset2)

# 4.3 역코딩을 위한 코딩 변경 

# [실습] 만족도(survey)를 긍정순서로 역 코딩 
survey <- dataset2$survey
csurvey <- 6-survey # 역코딩
csurvey

dataset2$survey <- csurvey # survery 수정
head(dataset2) # survey 결과 확인


# 5. 탐색적 분석을 위한 시각화 

# 5.1 범주형 vs 범주형

# [실습] 데이터 셋 가져오기 
setwd("c:/Rwork/Part-II")
new_data <- read.csv("new_data.csv", header=TRUE)
str(new_data)

# [실습] 범주형 vs 범주형 데이터 분포 시각화 
resident_gender <- table(new_data$resident2, new_data$gender2)
resident_gender
gender_resident <- table(new_data$gender2, new_data$resident2)
gender_resident

# 성별에 따른 거주지역 분포 현황 
barplot(resident_gender, beside=T, horiz=T,
        col = rainbow(5),
        legend = row.names(resident_gender),
        main = '성별에 따른 거주지역 분포 현황') 
# row.names(resident_gender) # 행 이름 

# 거주지역에 따른 성별 분포 현황 
barplot(gender_resident, beside=T, 
        col=rep(c(2, 4),5), horiz=T,
        legend=c("남자","여자"),
        main = '거주지역별 성별 분포 현황')  


# 5.2 연속형 vs 범주형

# [실습] 연속형 vs 범주형 데이터 분포 시각화 
install.packages("lattice")  # chap08
library(lattice)

# 직업유형에 따른 나이 분포 현황   
densityplot( ~ age, data=new_data, groups = job2,
             plot.points=T, auto.key = T)
# plot.points=T : 밀도, auto.key = T : 범례 


# 5.3 연속형 vs 범주형 vs 범주형  

# [실습] 연속형 vs 범주형 vs 범주형 데이터 분포 시각화 
# (1) 성별에 따른 직급별 구매비용 분석  
densityplot(~ price | factor(gender2), data=new_data, 
            groups = position2, plot.points=T, auto.key = T) 

# (2) 직급에 따른 성별 구매비용 분석  
densityplot(~ price | factor(position2), data=new_data, 
            groups = gender2, plot.points=T, auto.key = T) 
# 조건 : 직급(격자), 그룹 : 성별 


# 5.4 연속형(2개) vs 범주형(1개)  

# [실습] 연속형(2개) vs 범주형(1개) 
xyplot(price ~ age | factor(gender2), data=new_data) 


# 6. 파생변수 생성 

# 6.2 더미 형식으로 파생변수 생성 

# [실습] 주택 유형(단독주택, 다세대주태) : 0, 아파트 유형(아파트, 오피스텔) : 1 
# 데이터 파일 가져오기 
setwd('C:/Rwork/Part-II')
user_data <- read.csv('user_data.csv', header = T)
head(user_data) # user_id age house_type resident job 
table(user_data$house_type)

# 더미변수 생성 
house_type2 <- ifelse(user_data$house_type == 1 | user_data$house_type == 2, 0, 1)
house_type2[1:10] 

# 파생변수 추가 
user_data$house_type2 <- house_type2
head(user_data)


# 6.3 1:1 관계로 파생변수 생성 

# [실습] 고객식별번호(user_id) 대 상품 유형(product_type) 파생변수 생성 
# 데이터 파일 가져오기 
pay_data <- read.csv('pay_data.csv', header = T)
head(pay_data,10) # user_id product_type pay_method  price
table(pay_data$product_type)

# 고객별 상품 유형에 따른 구매금액 합계 파생변수 생성   
library(reshape2)
product_price <- dcast(pay_data, user_id ~ product_type, sum, na.rm=T) # 행 ~ 열 
head(product_price, 3) # 행(고객 id) 열(상품 타입)

# 칼럼명 수정 
names(product_price) <- c('user_id','식료품(1)','생필품(2)','의류(3)','잡화(4)','기타(5)')
head(product_price, 3) # 칼럼명 수정 확인 


# [실습] 고객식별번호(user_id) 대 고객지불유형(pay_method) 파생변수 생성

# 고객별 지불유형에 따른 구매상품 개수 파생변수 생성 
pay_price <- dcast(pay_data, user_id ~ pay_method, length) # 행 ~ 열 
head(pay_price, 3) # 행(고객 id) 열(상품 타입)

# 칼럼명 수정
names(pay_price) <- c('user_id','현금(1)','직불카드(2)','신용카드(3)','상품권(4)')
head(pay_price, 3) # 칼럼명 수정 확인 


# 6.4 파생변수 합치기 

# [실습] 고객정보 테이블에서 파생변수 추가 
library(plyr) # 패키지 로딩
user_pay_data <- join(user_data, product_price, by='user_id')
head(user_pay_data,10)

user_pay_data <- join(user_pay_data, pay_price, by='user_id')
user_pay_data[c(1:10), c(1,7:15)]

# [실습] 사칙연산으로 파생변수 생성 : 총 구매금액 파생변수 생성  
user_pay_data$총구매금액 <- user_pay_data$`식료품(1)` +user_pay_data$`생필품(2)`+user_pay_data$`의류(3)` +
  user_pay_data$`잡화(4)` + user_pay_data$`기타(5)`
head(user_pay_data)

user_pay_data[c(1:10), c(1, 7:11, 16)]


# 7. 표본 샘플링 


# 7.1 정제 데이터 저장

# [실습] 정제 데이터 저장하기
print(user_pay_data)          # 정제 데이터 확인
setwd("C:/Rwork/Part-II")     # 저장 폴더 지정
# 따옴표와 행 이름 제거하여 저장 
write.csv(user_pay_data, "cleanData.csv", quote=F, row.names=F) 
# 저장된 파일 불러오기/확인
data <- read.csv("cleanData.csv", header=TRUE)
data      # 저장된 파일 불러오기/확인


# 7.2 표본 추출하기

# [실습]  표본 추출하기 
nrow(data)       # data의 행수 구하기 -> Number of Rows
choice1 <- sample(nrow(data), 30) # 30개 무작위 추출
choice1          # 추출된 행 번호 출력
# 50~data 길이 사이에서 30개 무작위 추출
choice2 <- sample(50:nrow(data), 30) 
choice2
# 50~100 사이에서 30개 무작위 추출
choice3 <- sample(c(50:100), 30) 
choice3
# 다양한 범위를 지정해서 무작위 샘플링
choice4 <- sample(c(10:50, 80:150, 160:190), 30)
choice4

data[choice1, 1]

# [실습] iris 데이터 셋을 대상으로 7:3 비율로 데이터 셋 생성
data("iris")
dim(iris)

idx <- sample(1:nrow(iris), nrow(iris) * 0.7)
training <- iris[idx, ]      # 학습데이터 셋 
testing <- iris[-idx, ]     #　검정데이터 셋 
dim(training)                 # 105   5


# 7.3. 교차검정 샘플링 

# [실습]  데이터 셋을 대상으로 K겹 교차검정 데이터 셋 생성 
name <- c('a','b','c','d','e','f')
score <- c(90,85,70,85,60,74)
df <- data.frame(Name=name, Score=score)


install.packages('cvTools')
library(cvTools)

cross <- cvFolds(n=6, K=3, R = 1, type="random")
cross

str(cross)

# which를 이용하여 subsets 데이터 참조 
cross$subsets[cross$which==1,1] # K=1인 경우
cross$subsets[cross$which==2,1] # K=2인 경우
cross$subsets[cross$which==3,1] # K=3인 경우

r <- 1 # 1회전 
K <- 1:3 # 3겹 
for(k in K){ # 3회전 
  datas_idx <- cross$subsets[cross$which==k ,r]
  cat('k=', k, '검정데이터\n')
  print(df[datas_idx, ])

  cat('훈련데이터\n')
  print(df[-datas_idx, ])
}



