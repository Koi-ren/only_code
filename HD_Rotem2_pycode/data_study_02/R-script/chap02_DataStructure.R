# chap02_DataStructure

#####################################
## Chapter02. 데이터의 유형과 구조
#####################################

## 1. Vector 자료구조

# [실습] c() 함수 이용 벡터 객체 생성
c(1:20) # 콜론 : 범위 
1:20
c(1:5)

# [실습] seq() 함수 이용 벡터 객체 생성
seq(1,10,2) # 시작, 종료, 증감

# [실습]  rep() 함수 이용 벡터 생성
rep(1:3, 3) # 대상, 반복수  
rep(1:3, each = 3)


# [실습] setdiff()와 intersect() 함수 이용 
x <- c(1,3,5,7) 
y <- c(3,5)
x; y
union(x, y) # 합집합(x+y)
setdiff(x, y) # 차집합(x-y)
intersect(x, y) # 교집합(x^y)    

# [실습] 숫자형, 문자형, 논리형 벡터 생성 
v1 <- c(33,-5,20:23,12,-2:3)
v2 <-c("홍길동", "이순신", "유관순")
v3 <-c(T, TRUE, FALSE, T, TRUE,F,T)
v1;v2;v3
v4 <- c(33,-5,20:23,12,"4")
v4 # 합계 구하기 


# [실습] 한 줄에 명령문 중복사용
v1; mode(v1) 
v2; mode(v2)
v3; mode(v3)

# [실습] 벡터에 컬럼명 지정
age <- c(30,35,40)
age
names(age) <- c("홍길동", "이순신", "강감찬")
age
age <-NULL # age 변수 데이터 삭제


# [실습] 벡터 자료 참조하기
a <- c(1:50)
a[c(10:45)] # a[c(10:45)]
a[10 : (length(a)-5)] # 10~45

# [실습] 잘못된 벡터 첨자 사용 예
a[1, 2] # Error     

# [실습] c() 함수에서 콤마 사용 예
v1 <- c(33,-5,20:23,12,-2:3)
v1[1]
v1[c(2, 4)]
v1[c(3:5)]
v1[c(4, 5:8, 7)]

# [실습] 음수 값으로 첨자 지정 예
v1[-1]; v1[-c(2, 4)]; v1[-c(2:5)]; v1[-c(2, 5:10, 1)]


# [실습] 패키지 설치와 메모리 로딩
install.packages("RSADBE") # 패키지(데이터) 설치
library(RSADBE) # 패키지를 메모리에 로드
data(Severity_Counts) # RSADBE 패키지에서 제공되는 데이터 셋 가져오기
str(Severity_Counts) 

# [실습]  패키지에서 제공되는 데이터 셋 보기
Severity_Counts 


## 2. Matrix 자료구조

# [실습] 벡터 이용 행렬 객체 생성
m <- matrix(c(1:5))     
m

# [실습] 벡터의 열 우선으로 행렬 객체 생성
m <- matrix(c(1:10), nrow=2) 
m

# [실습] 행과 열의 수가 일치하지 않는 경우 예
m <- matrix(c(1:11), nrow=2)
m

# [실습]  벡터의 행 우선으로 행렬 객체 생성
m <- matrix(c(1:10), nrow=2, byrow=T) # 행 우선 
m

# [실습] 행 묶음으로 행렬 객체 생성
x1 <- c(5,40,50:52) 
x2 <- c(30,5,6:8) 
mr <- rbind(x1,x2) 
mr

# [실습] 열 묶음으로 행렬 객체 생성
mc <- cbind(x1,x2)  
mc

 
# [실습] 2행으로 행렬 객체 생성 
m3 <- matrix(10:19, 2) #10개 데이터를 2행으로 생성
m3
# 자료와 객체 Type 보기
mode(m3); class(m3) #numeric, matrix

# [실습] 행렬 객체에 첨자로 접근 
m3[1,] # 1행 전체
m3[,5] # 5열 전체
m3[2,3] #2행 3열의 데이터 1개 -> 15
m3[1, c(2:5)] # 1행에서 2~5열 데이터 4개


# [실습] 3행 3열로 행렬 객체 생성       
x <- matrix(c(1:9), nrow=3, ncol=3) # 3행 3열 matrix 객체
x

# [실습] 자료의 개수 보기
length(x) # 데이터 개수 
ncol(x); nrow(x) # 열/행 수


# [실습] apply() 함수 적용 
apply(x,1,max) # 행 단위 최대값
apply(x,1,min) # 행 단위 최대값
apply(x,2,mean) # 열 단위 평균값   

# [실습] 사용자 정의 적용
f <- function(x){ # x 매개변수 
  x * c(1,2,3)
}
result <- apply(x, 1, f)
result

# [실습] 열 우선 순서로 사용자 정의 함수 적용 
result <- apply(x, 2, f)
result

# [실습] 행렬 객체에 칼럼명 지정하기
colnames(x) <- c('one','two', 'three')
x

##  3. Array 자료구조 

# [실습] 배열 객체 생성하기
vec <- c(1:12) # 12개 벡터 객체 생성
arr <- array(vec, c(3,2,2)) # 3행2열2면 -> 3차원 배열 객체 생성
arr

# [실습] 배열 객체 자료 조회
arr[,,1] #1면 
arr[,,2] #2면 

# 배열 자료형과 자료구조 
mode(arr); class(arr) #numeric, array


# [실습] 데이터 셋 가져오기
library(RSADBE)
data(Bug_Metrics_Software) 
str(Bug_Metrics_Software)

# [실습] 데이터 셋 자료 보기
Bug_Metrics_Software


## 4. List 자료구조

# [실습] 1개 값을 갖는 리스트 객체 생성
list <- list("lee","이순신",95)
list # 전체 리스트 확인 


# [실습] 벡터 구조로 변경하기
unlist <- unlist(list)        
unlist

# [실습] 1개 이상의 값을 갖는 리스트 객체 생성
num <- list(c(1:5), c(6:10))
num

# [실습] key와 value 형식으로 리스트 생성  
member <- list(name=c("홍길동","유관순"),age = c(35, 25),
               address=c("한양","충남"),  
               gender=c("남자", "여자"), htype=c("아파트","오피스텔") )

member$name
member$name[1]
member$name[2]

# [실습] key를 이용하여 value에 접근하기 
member$age <- 45  # 원소 수정 
member$id <- "hong" # 원소 추가 
member$pwd <- "1234" # 원소 추가       
member

member$age <- NULL  # 원소 제거
member


# [실습] 리스트 객체에 함수 적용하기
# list data 처리 함수
a <- list(c(1:5))
b <- list(6:10)    

lapply(c(a,b), max) # list로 결과 반환

# [실습] 리스트 형식을 벡터 형식으로 반환하기
sapply(c(a,b), max)  # vactor로 결과 반환


# [실습] 다차원 리스트 객체 생성 
multi_list <- list(c1=list(1,2,3), c2=list(10,20,30), c3=list(100,200,300))
multi_list$c1; multi_list$c2; multi_list$c3


# [실습] 다차원 리스트를 열 단위로 바인딩
do.call(cbind, multi_list)
class(do.call(cbind, multi_list)) #  "matrix"


## 5. Data Frame 자료구조  

# [실습] 벡터 이용 객체 생성
no <- c(1,2,3)
name <- c("hong", "lee", "kim")
pay <- c(150,250,300)
vemp <- data.frame(NO=no, Name=name, Pay=pay) #컬럼명 지정 
vemp

# [실습] matrix 이용 객체 생성
m <- matrix(
  c(1,"hong",150,
    2, "lee", 250,
    3, "kim", 300) ,3 ,by=T) # 행우선, 3개 리스트 생성
memp <- data.frame(m)      
memp

# [실습] txt파일 이용 객체 생성
getwd()
setwd("C:/Rwork/Part-I") 
txtemp <- read.table('emp.txt', header=T, sep="") # 제목있음, 공백구분
txtemp


# [실습] csv파일 이용 객체 생성
csvtemp <- read.csv('emp.csv', header=T) # 제목있음, 컴마구분
csvtemp

name <- c("사번","이름","급여")
read.csv('emp2.csv', header=F, col.names=name)    

# [실습] 데이터프레임 만들기 
df <- data.frame( x=c(1:5), y=seq(2, 10, 2), z=c('a','b','c','d','e'))
df

# [실습] 데이터프레임 칼럼명 참조
df$x

# [실습] 자료구조, 열수, 행수, 칼럼명 보기
str(df)
ncol(df)
nrow(df)
df[c(2:3)]


# [실습] 요약 통계량 보기 
summary(df)

# [실습] 데이터프레임 자료에 함수 적용
apply(df[, c(1,2)], 2, sum)


# [실습] 데이터프레임의 부분 객체 만들기
x1 <- subset(df, x>=3) # x가 3이상인 레코드 대상       
x1

# [실습] 두 개의 조건으로 부분 객체 만들기
y1 <- subset(df, y<=8) # y가 8이하인 레코드 대상 
y1
xyand <- subset(df, x>=2 & y <= 6) # and -> 0
xyand
xyor <- subset(df, x>=2 | y<=6) # or -> 전체 
xyor


# [실습] student 데이터프레임 만들기
sid = c('A', 'B', 'C', 'D')
score = c(90, 80, 70, 60)
subject = c('컴퓨터', '국어국문', '소프트웨어', '유아교육')

student = data.frame(sid, score, subject)
student

# [실습] 자료형과 자료구조 보기
mode(student); class(student)
str(sid); str(score); str(subject)
str(student)

# [실습] 두 개 이상의 데이터프레임 병합하기 
height <- data.frame(id=c(1,2), h=c(180,175))
weight <- data.frame(id=c(1,2), w=c(80,75))

user <- merge(height, weight, by.x="id", by.y="id")
user

# [실습] galton 데이터 셋 가져오기   
install.packages("psych") #　패키지 설치
library(psych) # 패키지 로드
data(galton) # galton 데이터 셋 가져오기

# [실습] galton 데이터 셋 구조 보기 
str(galton) 
dim(galton)
head(galton, 20)


## 6. 문자열 처리

# [실습] 문자열 추출하기
install.packages("stringr")  # 패키지 설치
library(stringr) # 메모리 로딩

# 형식) str_extract('문자열', '정규표현식')
str_extract("홍길동35이순신45유관순25", "[1-9]{2}") # "12" -> 연속된 숫자2개 추출(첫번째)
str_extract_all("홍길동35이순신45유관순25", "[0-9]{2}") # "12" "33" -> 모두


# [실습] 반복수를 지정하여 영문자 추출 
string <- 'hongkildong105lee1002you25강감찬2005'
str_extract_all(string, '[a-z]{3}')  
str_extract_all(string, '[a-z]{3,}') 
str_extract_all(string, '[a-z]{3,5}') 
# 특정 단어 추출 
str_extract_all(string, '유관순')

# [실습] 한글, 영문자, 숫자 추출하기
str_extract_all(string, 'hong') 
str_extract_all(string, '25') 
str_extract_all(string, '[가-힣]{3}') 
str_extract_all(string, '[a-z]{3}') 
str_extract_all(string, '[0-9]{4}')


# [실습] 한글, 영문자, 숫자를 제외한 나머지 추출하기
str_extract_all(string, '[^a-z]')
str_extract_all(string, '[^a-z]{4}')
str_extract_all(string, '[^가-힣]{5}')
str_extract_all(string, '[^0-9]{3}')


# [실습] 주민등록번호 검사하기 
jumin <- '123456-3234567'
str_extract_all(jumin, '[0-9]{6}-[1234][0-9]{6}')
str_extract_all(jumin, '\\d{6}-[1234]\\d{6}')

# [실습] 지정된 길이의 단어 추출하기
name <- '홍길동1234,이순신5678,강감찬1012'
str_extract_all(name, '\\w{7,}')


# [실습] 문자열 길이 구하기 
string <- 'hongkild105lee1002you25강감찬2005'
len <- str_length(string) # 29


# [실습] 문자열 위치(index) 구하기 
string <- 'hongkild105lee1002you25강감찬2005'
str_locate(string, '강감찬') 

# [실습] 부분 문자열
string_sub <- str_sub(string, 1, len-7)
string_sub

string_sub <- str_sub(string, 1, 23)
string_sub

# [실습] 대문자, 소문자 변경하기 
str_to_upper(string_sub)
str_to_lower(string_sub)

# [실습] 문자열 교체하기 
string_rep <- str_replace(string_sub, 'hongkd105', '홍길동35,')
string_rep <- str_replace(string_sub, 'leess1002', '이순신45,')
string_rep <- str_replace(string_sub, 'you25', '유관순25,')
string_rep


# [실습] 문자열 결합하기 
string_c <- str_c(string_rep, '강감찬55')
string_c


# [실습] 문자열 분리하기
string_sp <- str_split(string_c, ',')
string_sp

# [실습] 문자열 합치기 
string_vec <- c('홍길동35', '이순신45', '유관순25', '강감찬55')
string_vec

string_join <- paste(string_vec, collapse = ',')
string_join


