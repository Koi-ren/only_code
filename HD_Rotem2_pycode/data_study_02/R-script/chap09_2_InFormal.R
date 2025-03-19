# chap09_2_InFormal

########################################
## Chapter09_2. 비정형데이터 처리 
########################################

# 2.1 토픽 분석  

# 텍스트마이닝을 위한 패키지 설치 
#install.packages("rJava")
Sys.setenv(JAVA_HOME='C:\\Program Files\\Java\\jre1.8.0_151')
library(rJava) # 로딩

# 토픽 분석을 위한 패키지 설치
install.packages(c("KoNLP", "wordcloud"))
# tm 패키지 구 버전 다운로드/설치 - version 3.3.2
install.packages("http://cran.r-project.org/bin/windows/contrib/3.0/tm_0.5-10.zip",repos=NULL)
install.packages('slam')
library(slam) 
library(tm) # tm 패키지는 slam 패키지에 의존적임 

# 패키지 로딩
library(KoNLP) # 세종사전 
library(tm) # 영문 텍스트 마이닝 
library(wordcloud) # RColorBrewer()함수 제공


# [실습] 명사 추출 예 
extractNoun('안녕하세요. 홍길동 입니다.')
extractNoun('텍스트마이닝이란 텍스트에서 유용한 정보를 찾아내는 과정을 말한다')


# [실습] 텍스트 자료 가져오기 
facebook <- file("C:/Rwork/Part-II/facebook_bigdata.txt", encoding="UTF-8")
facebook_data <- readLines(facebook) # 줄 단위 데이터 생성
head(facebook_data) # 앞부분 6줄 보기 - 줄 단위 문장 확인 
str(facebook_data) # chr [1:76]

# [실습] 자료집(Corpus) 생성 
facebook_corpus <- Corpus(VectorSource(facebook_data))
facebook_corpus 
inspect(facebook_corpus) # 76개 자료집에 포함된 문자 수 제공 


# [실습] 단어 추가와 단어추출 
#  (1) 세종 사전 사용 및 단어 추가
install.packages('curl')
library(curl)
useSejongDic() # 세종 사전 불러오기

# (2) 세종 사전에 없는 단어 추가
mergeUserDic(data.frame(c("R 프로그래밍","페이스북","소셜네트워크"), c("ncn"))) 
# ncn -명사지시코드

# [실습] 단어추출 사용자 함수 정의 
# (1) 사용자 정의 함수 작성 
exNouns <- function(x) { paste(extractNoun(as.character(x)), collapse=" ")}
# (2) exNouns 함수 이용 단어 추출 
facebook_nouns <- sapply(facebook_corpus, exNouns) 
facebook_nouns[1] # 단어만 추출된 첫 줄 보기 

# [실습] 추출된 단어 대상 전처리  
# (1) 추출된 단어 이용 자료집 생성
myCorputfacebook <- Corpus(VectorSource(facebook_nouns)) 
myCorputfacebook 
# (2) 데이터 전처리 
myCorputfacebook <- tm_map(myCorputfacebook, removePunctuation) # 문장부호 제거
myCorputfacebook <- tm_map(myCorputfacebook, removeNumbers) # 수치 제거
myCorputfacebook <- tm_map(myCorputfacebook, tolower) # 소문자 변경
myCorputfacebook <-tm_map(myCorputfacebook, removeWords, stopwords('english')) # 불용어제거
inspect( myCorputfacebook[1:5])

# [실습] 단어 선별(단어 길이 2개 이상)

# 전처리된 단어집을 대상으로 일반문서로 변환
myCorputfacebook_txt <- tm_map(myCorputfacebook, PlainTextDocument) 

# 단어길이 2개 이상인 단어만 선별하여 matrix 자료구조로 변경
myCorputfacebook_txt <- TermDocumentMatrix(myCorputfacebook_txt, control=list(wordLengths=c(2,Inf)))
myCorputfacebook_txt

# matrix 자료구조를 data.frame 자료구조로 변경
myTermfacebook.df <- as.data.frame(as.matrix(myCorputfacebook_txt)) 
dim(myTermfacebook.df) 


# [실습] 단어 빈도수 구하기 - 빈도수가 높은 순서대로 내림차순 정렬
wordResult <- sort(rowSums(myTermfacebook.df), decreasing=TRUE) # 빈도수로 내림차순 정렬
wordResult[1:10]

#  [실습] 단어 구름(wordcloud) 생성 - 디자인 적용 전
myName <- names(wordResult) # 단어 이름 생성 -> 빈도수의 이름 
wordcloud(myName, wordResult) # 단어구름 적성


# [실습] 불필요한 단어 제거 시작
# 1) 데이터 전처리  
myCorputfacebook <- tm_map(myCorputfacebook, removePunctuation) # 문장부호 제거
myCorputfacebook <- tm_map(myCorputfacebook, removeNumbers) # 수치 제거
myCorputfacebook <- tm_map(myCorputfacebook, tolower) # 소문자 변경
myStopwords = c(stopwords('english'), "사용", "하기");
myCorputfacebook = tm_map(myCorputfacebook, removeWords, myStopwords);
inspect(myCorputfacebook[1:5]) # 데이터 전처리 결과 확인

# 2) 단어 선별 - 단어 길이 2개 이상 단어 선별
myCorputfacebook_txt <- tm_map(myCorputfacebook, PlainTextDocument) 
myCorputfacebook_txt <- TermDocumentMatrix(myCorputfacebook_txt, control=list(wordLengths=c(2,Inf)))
myCorputfacebook_txt
# matrix -> data.frame 변경
myTermfacebook.df <- as.data.frame(as.matrix(myCorputfacebook_txt)) 
dim(myTermfacebook.df) # [1] 876  76

# 3) 단어 빈도수 구하기
wordResult <- sort(rowSums(myTermfacebook.df), decreasing=TRUE) # 빈도수로 내림차순 정렬
wordResult[1:10]


# 4) 단어 구름(wordcloud) 생성  생성 - 디자인 적용 전
myName <- names(wordResult) # 단어 이름 추출(빈도수 이름) 
wordcloud(myName, wordResult) # 단어구름 시각화 


# [실습] 단어 구름에 디자인 적용(빈도수, 색상, 위치, 회전 등) 
# (1) 단어이름과 빈도수로 data.frame 생성
word.df <- data.frame(word=myName, freq=wordResult) 
str(word.df) # word, freq 변수

# (2) 단어 색상과 글꼴 지정
pal <- brewer.pal(12,"Paired") # 12가지 색상 pal <- brewer.pal(9,"Set1") # Set1~ Set3
# 폰트 설정세팅 : "맑은 고딕", "서울남산체 B"
windowsFonts(malgun=windowsFont("맑은 고딕"))  #windows

# (3) 단어 구름 시각화 - 별도의 창에 색상, 빈도수, 글꼴, 회전 등의 속성 적용 
x11( ) # 별도의 창을 띄우는 함수
wordcloud(word.df$word, word.df$freq, 
          scale=c(5,1), min.freq=3, random.order=F, 
          rot.per=.1, colors=pal, family="malgun")



## 2.2 연관어 분석 

# [실습] 한글 처리를 위한 패키지 설치
#install.packages('rJava')
Sys.setenv(JAVA_HOME='C:\\Program Files\\Java\\jre1.8.0_151')
library(rJava) # 아래와 같은 Error 발생 시 Sys.setenv()함수로 java 경로 지정
install.packages("KoNLP") 
library(KoNLP) # rJava 라이브러리가 필요함


# [실습] 텍스트 파일 가져오기와 단어 추출하기 

# 1.텍스트 파일 가져오기
marketing <- file("C:/Rwork/Part-II/marketing.txt", encoding="UTF-8")
marketing2 <- readLines(marketing) # 줄 단위 데이터 생성
# incomplete final line found on - Error 발생 시 UTF-8 인코딩 방식으로 재 저장
close(marketing) 


# 2. 줄 단위 단어 추출
lword <- Map(extractNoun, marketing2)  
length(lword) # [1] key = 472

lword <- unique(lword) # 중복제거1(전체 대상)
length(lword) # [1] 353(19개 제거)

# 3. 중복단어 제거와 추출 단어 확인
lword <- sapply(lword, unique) # 중복제거2(줄 단위 대상) 
length(lword) # [1] 352(1개 제거)


# [실습] 연관어 분석을 위한 전처리 

# 1) 단어 필터링 함수 정의
filter1 <- function(x){
  nchar(x) <= 4 && nchar(x) >= 2 && is.hangul(x)
}
 
filter2 <- function(x){
  Filter(filter1, x)
}

# 2) 줄 단위로 추출된 단어 전처리 
lword <- sapply(lword, filter2)
lword

# [실습] 필터링 간단 예문

# 1) vector 이용 list 객체 생성
word <- list(c("홍길동","이순","만기","김"), 
             c("대한민국","우리나라대한민국","한국","resu"))   # 영문자 포함 
class(word) 

# 2) 단어 필터링 함수 정의(길이 2~4 사이인 한글 단어추출) 
filter1 <- function(x) {  
  nchar(x) <= 4 && nchar(x) >= 2 && is.hangul(x) 
} 
filter2 <- function(x) { 
  Filter(filter1, x) 
}

# 3) 함수 적용 list 객체 필터링 
filterword <- sapply(word, filter2)
filterword


# [실습] 트랜잭션 생성

# 1) 연관분석을 위한 패키지 설치
install.packages("arules")
library(arules) 

# 2) 트랜잭션 생성 
wordtran <- as(lword, "transactions") # lword에 중복데이터가 있으면 error발생
wordtran 


# [실습] 단어 간 연관규칙 산출
tranrules <- apriori(wordtran, parameter=list(supp=0.25, conf=0.05)) 

# [실습] 연관규칙 생성 결과보기 
inspect(tranrules) # 연관규칙 생성 결과(59개) 보기

# [실습] 연관규칙 생성 간단 예문 
data(Adult)
Adult
str(Adult) 
dim(Adult)   # 차원보기 : 48,842개 트랜잭션과 115개 아이템 

apr1 <- apriori(Adult, parameter = list(support= 0.1, target="frequent"), 
                appearance = list(none = c("income=small", "income=large"), 
                                  default="both")) 
apr1
inspect(apr1) 

apr2 <- apriori(Adult, parameter = list(support= 0.1, target="rules"), 
                appearance = list(none = c("income=small", "income=large"), 
                                  default="both"))

apr3 <- apriori(Adult, parameter = list(support= 0.5, conf = 0.9, target="rules"), 
                appearance = list(none = c("income=small", "income=large"), 
                                  default="both"))

# [실습]  연관어 시각화 

# 1) 연관단어 시각화를 위해서 자료구조 변경
rules <- labels(tranrules, ruleSep=" ")  
rules
class(rules)

# 2) 문자열로 묶인 연관단어를 행렬구조 변경 
rules <- sapply(rules, strsplit, " ",  USE.NAMES=F) 
rules
class(rules) 

# 3) 행 단위로 묶어서 matrix로 반환
rulemat <- do.call("rbind", rules)
rulemat
class(rulemat)

# [실습] 연관어 시각화를 위한 igraph 패키지 설치
install.packages("igraph") # graph.edgelist(), plot.igraph(), closeness() 함수 제공
library(igraph)   

# [실습] edgelist보기 - 연관단어를 정점 형태의 목록 제공 
ruleg <- graph.edgelist(rulemat[c(12:59),], directed=F) # [1,]~[11,] "{}" 제외
ruleg

# [실습] edgelist 시각화
X11()
plot.igraph(ruleg, vertex.label=V(ruleg)$name,
            vertex.label.cex=1.2, vertex.label.color='black', 
            vertex.size=20, vertex.color='green', vertex.frame.color='blue')


