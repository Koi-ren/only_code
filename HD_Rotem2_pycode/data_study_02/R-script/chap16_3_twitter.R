# chap16_3_Twitter

#########################################
## Chapter16_3. twitter 데이터 크롤링
#########################################

## [실습] Twitter 앱 인증 요청 및 인증 완료

# 단계 1 :  Twitter 앱 인증 요청 및 인증 수행을 위한 패키지 설치 및 로딩
install.packages("twitteR")  
install.packages("ROAuth")  
install.packages("base64enc")
library(twitteR)
library(ROAuth) 
library(base64enc)

# 단계 2 :  Twitter 앱 요청 URL과 API 설정
# [Details] - 3개 url 변수 생성
reqURL <- "https://api.twitter.com/oauth/request_token"
authURL <- "https://api.twitter.com/oauth/authorize"
accessURL <- "https://api.twitter.com/oauth/access_token"

# [Keys and Access Tokens] - 4개 변수 : ##Site에서 받아온다.
apiKey <-  "bINvDLa0dsPbo2la8PiscuUqC" 
apiSecret <- "PKNHc2ls7cnuFPbD0eWYxqXi7QMK2WCucWjYLWShZMQPu77SNS" 
accessToken="632641860-hADhYcejnc2AlMFxFKy7E2BwLmsLsZGiMjaStMcm"
accessTokenSecret="D4m5xjaihndouW4FLg3LxVxBUitRmSjKJBephvmkRL8x5"

# 단계 3 : Twitter 앱 인증 요청
twitCred <- OAuthFactory$new(
  consumerKey = apiKey, 
  consumerSecret = apiSecret,
  requestURL = reqURL,
  accessURL = accessURL, 
  authURL = authURL
)

# 단계 4 : Twitter 앱 인증 수행
twitCred$handshake(
  cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl")
)

# 단계 5 : Twitter 앱 인증을 위한 PIN 받기
setup_twitter_oauth(apiKey, 
                    apiSecret,
                    accessToken,
                    accessTokenSecret)
# 함수 실행 -> 선택: 1(1: Yes)


## [실습] Twitter 앱에 접근하여 데이터 가져오기

# 단계 1 : 검색어 입력과 검색 결과 받기 
keyword <- enc2utf8("빅데이터") # UTF-8 인코딩 방식 지정 - base 패키지 
test <- searchTwitter(keyword, n=300) # twitteR 패키지 제공 
test
class(test) # [1] "list"

# 단계 2 :  list 자료구조를 vector 자료구조로 변경
test_vec <- vector() # vector 객체 생성 
n <- 1: length(test)

for(i in n){
  test_vec[i] <- test[[i]]$getText()
}
test_vec

# data type과 구조보기 
class(test_vec); str(test_vec)

# 단계 3 : 파일 저장 및 가져오기
write.csv(test_vec, "c:/Rwork/output/test.txt", quote = FALSE, row.names = FALSE)
test_txt <- file("C:/Rwork/output/test.txt")
twitter <- readLines(test_txt)
str(twitter)


## [실습] Twitter 검색 데이터 대상 연관어 분석

# 단계 1 : 한글 처리를 위한 패키지 설치
Sys.setenv(JAVA_HOME='C:\\Program Files\\Java\\jre1.8.0_151')
library(rJava) # 아래와 같은 Error 발생 시 Sys.setenv()함수로 java 경로 지정
library(KoNLP) # rJava 라이브러리가 필요함

# 단계 2 :  줄 단위 단어 추출
lword <- Map(extractNoun, twitter) 
length(lword) 
lword <- unique(lword) # 중복제거1(전체 대상)
length(lword) 
lword <- sapply(lword, unique) # 중복제거2(줄 단위 대상) 
length(lword) 
lword # 추출 단어 확인

# 단계 3 :  데이터 전처리
# (1) 길이가 2~4 사이의 단어 필터링 함수 정의
filter1 <- function(x){
  nchar(x) <= 4 && nchar(x) >= 2 && is.hangul(x)
}
# (2) Filter(f,x) -> filter1() 함수를 적용하여 x 벡터 단위 필터링 
filter2 <- function(x){
  Filter(filter1, x)
}

# (3) 줄 단어 대상 필터링
lword <- sapply(lword, filter2)
lword # 추출 단어 확인(길이 1개 단어 삭제됨)

# 단계 4 : 트랜잭션 생성 : 연관분석을 위해서 단어를 트랜잭션으로 변환
library(arules) 
wordtran <- as(lword, "transactions") # lword에 중복데이터가 있으면 error발생
wordtran 
inspect(wordtran)  # 트랜잭션 내용 보기

# 단계 5 : 단어 간 연관규칙 산출
tranrules <- apriori(wordtran, parameter=list(supp=0.09, conf=0.8))  # 54 rule(s)
inspect(tranrules) # 연관규칙 생성 결과(23개) 보기

# 단계 6 : 연관어 시각화 
# (1) 데이터 구조 변경 : 연관규칙 결과 -> 행렬구조 변경(matrix 또는 data.frame) 
rules <- labels(tranrules, ruleSep=" ") # 연관규칙 레이블을 " "으로 구분하여 변경   
rules # 예) 59 {경영,마케팅}   => {자금} -> 59 "{경영,마케팅} {자금}"
class(rules)

rules <- sapply(rules, strsplit, " ",  USE.NAMES=F) 
rules
class(rules) 

# 행 단위로 묶어서 matrix로 반환
rulemat <- do.call("rbind", rules)
rulemat
class(rulemat)

# (2) 연관어 시각화를 위한 igraph 패키지 설치
library(igraph)   

# (3) edgelist보기 - 연관단어를 정점 형태의 목록 제공 
ruleg <- graph.edgelist(rulemat[c(1:54),], directed=F) 

# (4) edgelist 시각화
X11()
plot.igraph(ruleg, vertex.label=V(ruleg)$name,
            vertex.label.cex=1.0, vertex.label.color='black', 
            vertex.size=20, vertex.color='green', vertex.frame.color='blue')
