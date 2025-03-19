# chap03_DataIO

#####################################
## Chapter03. 데이터 입출력 
#####################################

# 1. 데이터 불러오기

## 1-1. 키보드 입력

# [실습] 키보드로 숫자 이력하기 
num <- scan()
num 

# 합계 구하기
sum(num) 

# [실습] 키보드로 문자 입력하기
name <- scan(what=character())
name  

# [실습] 편집기 이용 데이터프레임 만들기
df = data.frame() #빈 데이터프레임 생성
df = edit(df) # 데이터 편집기
df

## 1-2. 로컬 파일 가져오기 

# 1) read.table() 함수 이용

# [실습]  컬럼명이 없는 파일 불러오기
getwd()
setwd("C:/Rwork/Part-I")
student  <- read.table(file="student.txt")
student

names(student) <- c('번호', '이름', '키', '몸무게')
student

# [실습] 컬럼명이 있는 파일 불러오기
student1  <- read.table(file="student1.txt", header=TRUE)
student1

# [실습] 탐색기를 통해서 파일 선택하기
student1  <- read.table(file.choose(), header=TRUE)

# [실습] 구분자가 있는 경우(세미콜론, 탭)
student2  <- read.table(file="student2.txt", sep=";", header=TRUE) # 세미콜론
student2  <- read.table(file="student2.txt", sep="\t", header=TRUE)

# [실습]  결측치를 처리하여 파일 불러오기
student3 <- read.table(file="student3.txt", sep=" ", header=TRUE, 
                       na.strings="-") # 문자열 -> NA 처리 
student3


# [실습]  csv 파일 형식 불러오기 
student4 <- read.csv(file="student4.txt", na.strings="-")
student4


# read.xlsx() 함수 이용 - 엑셀데이터 읽어오기

# [실습] 패키지 설치와 java 실행환경설정
install.packages("xlsx")   # xlsx 패키지 설치 
install.packages("rJava")   # rJava 패키지 설치 
Sys.setenv(JAVA_HOME='C:\\Program Files\\Java\\jre1.8.0_151')


# [실습] 관련 패키지 메모리 로드
library(rJava) # 로딩
library(xlsx) # 로딩

# [실습] 엑셀 파일 가져오기
studentex <- read.xlsx(file.choose(), 
                       sheetIndex=1, encoding="UTF-8")
studentex


## 1-3.  인터넷에서 파일 가져오기  

# 단계 1 : 세계 GDP 순위 데이터 가져오기 
GDP_ranking <- read.csv('http://databank.worldbank.org/data/download/GDP.csv')
GDP_ranking
head(GDP_ranking, 10)

# 데이터를 가공하기 위해 불필요한 행과 열을 제거한다.
GDP_ranking2 <- GDP_ranking[-c(1:4), c(1,2,4,5)]
head(GDP_ranking2)

# 상위 15개 국가 선별한다.
GDP_ranking15 <- head(GDP_ranking2, 15) # 상위 15국가 
GDP_ranking15

# 데이터프레임을 구성하는 4개의 열에 열 이름을 지정한다.
names(GDP_ranking15) <- c('Code', 'Ranking','Nation','GDP')
head(GDP_ranking15)


# 단계 2 : 세계 GDP 상위 15위 국가 막대 차트 시각화 
gdp <- GDP_ranking15$GDP
nation <- GDP_ranking15$Nation


library(stringr)
num_gdp <- as.numeric(str_replace_all(gdp, ',', ''))
num_gdp

GDP_ranking15$GDP <- num_gdp

# 막대차트 시각화 
barplot(GDP_ranking15$GDP, col = rainbow(15), 
        xlab = '국가(nation)', ylab='단위(달러)', names.arg = nation)

# 1,000단위 축소
num_gdp2 <- num_gdp/1000           
GDP_ranking15$GDP2 <- num_gdp2
barplot(GDP_ranking15$GDP2, col = rainbow(15), 
               main="2017년도 GDP 세계 15위 국가",
               xlab = '국가(nation)', ylab='단위(달러)', names.arg = nation)


## 1-4. 웹문서 가져오기 

# [실습] 2010년~2015년도 미국의 주별 1인당 소득 자료 가져오기

# 단계 1 : XML 패키지 설치
install.packages("XML")
install.packages("httr") # package 추가 
library(XML)
library(httr)

# 단계 2 : 미국의 주별 1인당 소득 자료 가져오기
url <- "http://ssti.org/blog/useful-stats-capita-personal-income-state-2010-2015"
get_url <- GET(url) # httr 제공 
get_url$content # 16 진수 
rawToChar(get_url$content) # html 태그 변환  
html_cont <- readHTMLTable(rawToChar(get_url$content), stringsAsFactors = F)
str(html_cont) # list

# 단계 3 : 자료구조 변경과 칼럼을 포함한 앞부분 6개 관측치 보기
html_cont = as.data.frame(html_cont) # data.frame형 변환 
str(html_cont) # list
head(html_cont)

# 단계 4 : 칼럼명을 수정한 후 뒷부분 6개 관측치 보기
names(html_cont) <- c("State",'y2010','y2011','y2012','y2013','y2014','y2015')
tail(html_cont)


# 2. 데이터 저장하기

# 2-1. 화면(콘솔) 출력

# 1) cat() 함수
x <- 10
y <- 20
z <- x * y
cat("x*y의 결과는 ", z ," 입니다.\n")  # \n 줄바꿈
cat("x*y = ", z)

# 2) print() 함수
print(z) # 변수 또는 수식만 가능
print(z*10)
print('x*y =', z) # Error


# 2-2. 파일에 데이터 저장

# 1) sink() 함수를 이용 파일 저장
setwd("C:/Rwork/output")       # 작업 디렉터리 변경 
library(RSADBE)               # 패키지를 메모리에 로드
data(Severity_Counts)          # Severity_Counts 데이터 셋 가져오기
sink("severity.txt")             # 저장할 파일 open
severity <- Severity_Counts   # 데이터 셋을 변수에 저장  
severity                       # 콘솔에 출력되지 않고 파일에 저장
sink() # 오픈된 파일 close


# 2) write.table()함수 이용 파일 저장
# 단계 1 : 탐색기를 이용하여 데이터 가져오기
setwd("C:/Rwork/output")         # 작업 디렉토리 지정
# C:/RWork/studentexcel.xlsx 파일선택
studentx <- read.xlsx(file.choose(), sheetIndex=1, encoding="UTF-8") 
# 단계 2 : 기본속성으로 저장 - 행 이름과 따옴표가 붙는다.
write.table(studentx, "stdt.txt")    # 행 번호와 따옴표 출력
# 단계 3 : ‘row.names=FALSE’ 속성을 이용하여 행 이름 제거하여 저장한다.
write.table(studentx, "stdt2.txt", row.names=FALSE)  # 행 번호 제거
# 단계 4 : ‘quote=FALSE’ 속성을 이용하여 따옴표를 제거하여 저장한다.
write.table(studentx, "stdt3.txt", row.names=FALSE, quote=FALSE) 

GDP_ranking15            # 데이터프레임 확인
setwd("C:/Rwork/output")     #　저장할 작업 디렉터리 지정
write.table(GDP_ranking15, "GDP_ranking15.txt", row.names=F) 

GDP_ranking15 <- read.table(file="GDP_ranking15.txt", sep="", header=T) 
GDP_ranking15

# 3) write.xlsx() 함수 이용 파일 저장 - 엑셀 파일로 저장
library(xlsx) # excel data 입출력 함수 제공

# studentexcel.xlsx 파일 선택
st.df <- read.xlsx(file.choose(), sheetIndex=1, encoding="UTF-8")
st.df
write.xlsx(st.df, "studentx.xlsx") # excel형식으로 저장
  
# 4) write.csv() 함수 이용 파일 저장
# data.frame 형식의 데이터를 csv 형식으로 저장
setwd("C:/Rwork/output")
st.df
write.csv(st.df,"stdf.csv", row.names=F, quote=F) # 행 이름 제거

