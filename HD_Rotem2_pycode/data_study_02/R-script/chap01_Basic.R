## chap01_Basic

#####################################
## Chapter01. R 설치와 개요
#####################################
# 주요 단축키 
# script 실행 :  Ctrl + Enter, Ctrl + R 
# 자동완성 : Ctrl + space
# 저장 : Ctrl + S


## 3. 패키지와 Session 보기

# [실습] R 패키지 보기
dim(available.packages())
available.packages()

# [실습] R 세션 보기
sessionInfo() 
# version, 다국어(locale) 정보, 설치된 패키지(7개) 

# [실습] 패키지 사용법 
install.packages("stringr") # "패키지명"
install.packages()  # 패키지 설치 확인 
library(stringr) # 메모리 로딩 
search() # 패키지 메모리 로딩 확인 

# [실습] 패키지 제거 
remove.packages('stringr')

# [실습] 데이터 셋 보기
data() 

# [실습] 기본 데이터 셋으로 히스토그램 그리기
# 단계 1 : 빈도수(frequency)를 기준으로 히스토그램 그리기
hist(Nile)  
# 단계 2 : 밀도(density)를 기준으로 히스토그램 그리기 
hist(Nile, freq = F) # frequency 속성을 FALSE로 지정 
# 단계 3 : 단계 2의 결과에 분포곡선(line)을 추가 
lines(density(Nile)) 

# [실습] 히스토그램을 파일에 저장하기
par(mfrow=c(1,1)) # Plots 영역에 1개 그래프 표시 
pdf("C:/Rwork/batch.pdf") # 지정된 경로의 파일에 결과 출력
hist(rnorm(20)) # 난수에 대한 히스토그램 그리기 
dev.off()   


## 4. 변수와 자료형

# [실습] 변수 사용 예
var1 <- 0 # 변수 var1에 값 0으로 초기화 (var1 = 0 사용 가능) 
var1 # 변수 var1의 값을 확인 즉, var1 변수값을 콘솔에 출력한다. 
var1 <- 1  # 변수 var1의 값을 1로 변경(변수 재사용) 
var1 # 변수 var1의 값을 확인 
var2 <- 2  # 변수 var2를 생성하고 값 2로 초기화 
var2 # 변수 var2의 값을 확인 
var3 <- 3 # 변수 var3을 생성하고 값 3으로 초기화 
var3 # 변수 var3의 값을 확인

# [실습] '변수.멤버' 형태로 변수선언 예
goods.code <- 'a001' # 상품 코드 
goods.name <- '냉장고'  # 상품명 
goods.price <- 850000  # 가격 
goods.des <- "최고사양, 동급 최고 품질"  # 상품설명

# [실습] 스칼라 변수 사용 예
age <- 35 
name <- "홍길동" 
age # 정수 35를 갖는 스칼라 변수의 값 확인 
name # 문자열 '홍길동'을 갖는 스칼라 변수의 값 확인

# [실습] 자료형 관련 실습
int <- 20 # 숫자형 
string <- "홍길동" # 문자형 
boolean <- TRUE # T or FALSE(F)
sum(10,20,30)
sum(10,20,20, NA)
sum(10,20,20,NA, na.rm = T)
ls()

# [실습] 자료형 확인 
is.character(string)
x <- is.numeric(int)
x
is.logical(boolean)
is.logical(x) 
is.na(x)


# [실습] 문자 원소를 숫자 원소로 형 변환
x <- c(1, 2, "3")
x
result <- as.numeric(x) # 문자열 -> 숫자형 
result

# [실습] 복소수형 자료 생성과 형 변환 
z <- 5.3 - 3i
Re(z)
Im(z)
is.complex(z)
as.complex(5.3)

# [실습] 스칼라 변수의 자료형과 자료구조 확인
mode(int)
mode(string)
mode(boolean)
class(int)
class(string)
class(boolean)


# [실습] 문자 벡터와 그래프 생성 
gender <- c('man', 'woman', 'woman', 'man', 'man')
plot(gender)

# [실습]  as.factor() 함수 이용 요인형 변환
Ngender <- as.factor(gender)
table(Ngender)

# [실습] Factor형 변수로 차트 그리기 
plot(Ngender)
mode(Ngender)
class(Ngender)
is.factor(Ngender)

# [실습] Factor Nominal 변수 내용 보기
Ngender 

# [실습] factor() 함수 이용 Factor형 변환
args(factor)
Ogender <- factor(gender, levels = c('woman', 'man'), ordered = T)
Ogender

# [실습] 순서 없는 요인과 순서 있는 요인형 변수로 차트 그리기
par(mfrow=c(1, 2)) 
plot(Ngender) 
plot(Ogender)

# [실습] as.Data() 함수 이용 날짜형 변환
as.Date('17/02/28', '%y/%m/%d')
class(as.Date('17/02/28', '%y/%m/%d'))
datas <- c('02/28/17', '02/29/17', '03/01/17')
as.Date(datas, '%m/%d/%y')

# [실습] 시스템의 로케일 정보 확인
Sys.getlocale(category = 'LC_ALL')
Sys.getlocale(category = 'LC_COLLATE')

# [실습] 현재 날짜와 시간 확인 
Sys.time()

# [실습] strptime() 함수 이용 날짜형 변환
sdate <- '2015-11-11 12:47:5'
class(sdate)

today <- strptime(sdate, format = "%Y-%m-%d %H:%M:%S")
today
class(today)

# [실습] 4자리 년도와 2자리 연도 표기의 예
strptime('01-05-2015', format = "%d-%m-%Y")
strptime('01-05-15', format = "%d-%m-%y")

# [실습] 국가별 로케일(locale) 설정
Sys.setlocale(category = "LC_ALL", locale = "") 
Sys.setlocale(category = "LC_ALL", locale = "Korean_Korea")     
Sys.setlocale(category = "LC_ALL", locale = "English_US")
Sys.setlocale(category = "LC_ALL", locale = "Japanese_Japan")  
Sys.getlocale()   

# [실습] 미국식 날짜표현 -> 한국식 날짜표현
Sys.setlocale(category = 'LC_ALL', locale = 'English_USA') # 미국식 
strptime('01-jan-15', format = '%d-%b-%y')
day <- strptime('Saturday, 23 Jan 2016', format = '%A, %d %b %Y') # 전체 요일 
day <- strptime('Sat, 23 Jan 2016', format = '%a, %d %b %Y') # 약자 요일
weekdays(day) # 요일 보기 
# 약자 월과 2자리 년도 
strptime('23 Mar 18', format = '%d %b %y')
day <- c('1may99', '2jun01', '28jul15')
strptime(day, format = '%d%b%y')
 

## 5. 기본함수와 작업공간 

# 도움말 보기 
help(sum)
?sum

# [실습] 함수 파라미터 보기
args(sum)

# [실습]  함수 사용 예제 보기
example(seq)

# [실습] 평균을 구해주는 mean() 함수 사용 예
example(mean)

# 작업공간 
getwd() 
setwd('C:/Rwork/Part-I') 
test <- read.csv('test.csv')
test





