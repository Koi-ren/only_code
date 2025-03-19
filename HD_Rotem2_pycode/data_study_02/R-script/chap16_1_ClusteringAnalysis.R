# chap16_1_ClusteringAnalysis

######################################
## Chapter16_1. ClusteringAnalysis
######################################

## 1. 유클리드안 거리
# 유클리드 거리(Euclidean distance)는 두 점 사이의 거리를 계산하는 
# 방법으로 이 거리를 이용하여 유클리드 공간을 정의한다.

# [실습] 유클리디안 거리 계산법

# 단계 1 : matrix 객체 생성
x <- matrix(1:9, nrow=3, by=T) 
x

# 단계 2 : 유클리드안 거리 생성
dist <- dist(x, method="euclidean") # method 생략가능
dist


# (3) 유클리드 거리 계산식의 R코드

# 1행과 2행 변량의 유클리드 거리 구하기
sqrt(sum((x[1,] - x[2, ])^2)) # 5.196152
# 1행과 3행 변량의 유클리드 거리 구하기
sqrt(sum((x[1,] - x[3, ])^2)) # 10.3923


## 2. 계층적 군집분석(탐색적 분석)

# [실습] 유클리디안 거리를 이용한 군집화

# 단계 1 : 군집분석(Clustering)분석을 위한 패키지 설치
install.packages("cluster") 
library(cluster) 

# 단계 2 :  데이터 셋 생성
x <- matrix(1:9, nrow=3, by=T) 
x

# 단계 3 : matrix 대상 유클리드 거리 생성 함수
dist <- dist(x, method="euclidean") # method 생략가능
dist

# 단계 4 : 유클리드 거리 matrix를 이용한 클러스터링
hc <- hclust(dist) # 클러스터링 적용
hc
# 단계 5 : 클러스터 시각화 
plot(hc) # 1과2 군집(클러스터) 형성


# [실습] 신입사원 면접시험 결과 군집분석

# 단계 1 : 데이터 셋 가져오기
interview <- read.csv("c:/Rwork/Part-IV/interview.csv", header=TRUE)
names(interview)

# 단계 2 : 유클리디안 거리 계산 
interview_df <- interview[c(2:7)]
idist<- dist(interview_df) # no 제거 
head(idist)

# 단계 3 : 계층적 군집분석
hc <- hclust(idist)
hc

# 단계 4 : 군집분석 시각화
plot(hc, hang=-1) 

# 단계 5 :  군집 단위 테두리 생성 
rect.hclust(hc, k=3, border="red") # 3개 그룹 선정, 선 색 지정

## [실습] 군집별 특징 보기 

# 단계 1 : 각 그룹별 서브셋 만들기
g1<- subset(interview, no==109| no==103| no==111| no==105 | no==114)
g2<- subset(interview, no==113| no==102| no==106| no==101 | no==104)
g3<- subset(interview, no==115| no==108| no==110| no==107 | no==112)

# 단계 2 : 그룹 요약통계량  
table(interview$no)
summary(g1) # 불합격:5
summary(g2) # 합격:5
summary(g3) # 불합격:5


##  3. 군집수 자르기
# [실습] iris 데이터 셋을 대상으로 군집수 자르기 

# 단계 1 : 유클리드안 거리 계산 
idist<- dist(iris[1:4]) # dist(iris[, -5])

# 계층형 군집분석(클러스터링)
hc <- hclust(idist)
hc
plot(hc, hang=-1)
rect.hclust(hc, k=4, border="red") # 4개 그룹수 

# 단계 2 :  군집수 자르기
ghc<- cutree(hc, k=3) # stats 패키지 제공
ghc #  150개(그룹을 의미하는 숫자(1~3) 출력)

# 단계 3 : iris에서 ghc 컬럼 추가
iris$ghc <- ghc
head(iris)
table(iris$ghc) # ghc 빈도수
head(iris,60) # ghc 칼럼 확인 

# 단계 4 : 요약통계량 구하기
g1 <- subset(iris, ghc==1)
summary(g1[1:4])

g2 <- subset(iris, ghc==2)
summary(g2[1:4])

g3 <- subset(iris, ghc==3)
summary(g3[1:4])


## 4. 비계층적 군집분석 

# 단계 1 : 군집분석에 사용할 변수 추출 
library(ggplot2)
data(diamonds)
t <- sample(1 : nrow(diamonds),1000) # 1000개 셈플링 
test <- diamonds[t, ] # 1000개 표본 추출
dim(test) # [1] 1000 10

head(test) # 검정 데이터
mydia <- test[c("price","carat", "depth", "table")] # 4개 칼럼만 선정
head(mydia)

# 단계 2 : 계층적 군집분석(탐색적 분석)
result <- hclust(dist(mydia), method="average") # 평균거리 이용 
result

# 군집 방법(Cluster method) 
# method = "complete" : 완전결합기준(최대거리 이용) <- default(생략 시)
# method = "single" : 단순결합기준(최소거리 이용) 
# method = "average" : 평균결합기준(평균거리 이용) 

plot(result, hang=-1) # hang : -1 이하 값 제거

# 단계 3 :  비계층적 군집분석
result2 <- kmeans(mydia, 3)
names(result2) # cluster 칼럼 확인 

result2$cluster # 각 케이스에 대한 소속 군집수(1,2,3)
result2$centers # 각 군집 중앙값

# 원형데이터에 군집수 추가
mydia$cluster <- result2$cluster
head(mydia) # cluster 칼럼 확인 

# 단계 4 :  변수 간의 상관계수 보기 
cor(mydia[,-5], method="pearson") # 상관계수 보기 
plot(mydia[,-5])

 # 상관계수 색상 시각화 
install.packages('mclust')
library(mclust)
library(corrgram) # 상관성 시각화 
corrgram(mydia[,-5]) # 색상 적용 - 동일 색상으로 그룹화 표시
corrgram(mydia[,-5], upper.panel=panel.conf) # 수치(상관계수) 추가(위쪽)


# 단계 5 : 비계층적 군집시각화
plot(mydia$carat, mydia$price, col=mydia$cluster)
# 중심점 표시 추가 
points(result2$centers[,c("carat", "price")], col=c(3,1,2), pch=8, cex=5)

