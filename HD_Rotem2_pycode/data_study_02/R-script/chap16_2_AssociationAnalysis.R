# chap16_2_AssociationAnalysis

#################################################
## Chapter16_2. 연관분석(Association Analysis)
#################################################
# 연관분석은 군집분석에 의해서 그룹핑된 cluster를 대상으로 해당
# 그룹에 대한 특성을 분석하는 방법으로 장바구니 분석으로 알려짐
# 즉 유사한 개체들을 클러터로 그룹화하여 각 집단의 특성 파악
# 대용량 데이터베이스에서는 전체 데이터를 유사한 클러스터로 
# 묶어서 관찰 및 분석하는 것이 더 효율적이다.

# 특징
# - 데이터베이스에서 사건의 연관규칙을 찾는 무방향성 데이터마이닝 기법                                            
# - 무방향성(x -> y변수 없음) -> 비지도 학습에 의한 패턴 분석 방법
# - 사건과 사건 간 연관성(관계)를 찾는 방법(예:기저귀와 맥주)
# - A와 B 제품 동시 구매 패턴(지지도)
# - A 제품 구매 시 B 제품 구매 패턴(신뢰도)


# 예) 장바구니 분석 : 장바구니 정보를 트랜잭션(상품 거래 정보)이라고 하며,
# 트랜잭션 내의 연관성을 살펴보는 분석기법
# 분석절차 : 거래내역 -> 품목 관찰 -> 상품 연관성에 대한 규칙(Rule) 발견

# 활용분야
# - 대형 마트, 백화점, 쇼핑몰 등에서 고객의 장바구니에 들어있는 품목 간의 
#   관계를 탐구하는 용도
# ex) 고객들은 어떤 상품들을 동시에 구매하는가?
#   - 맥주를 구매한 고객은 주로 어떤 상품을 함께 구매하는가?

# - 대형 마트,백화점, 쇼핑몰 판매자 -> 고객 대상 상품추천, 마케팅
# 1) 고객 대상 상품추천 및 상품정보 발송  
#     -> ex) A고객에 대한 B 상품 쿠폰 발송
# 2) 텔레마케팅를 통해서 패키지 상품 판매 기획 및 홍보 
# 3) 상품 진열 및 show window 상품 display


## 1. 연관규칙 평가 척도

# 연관규칙의 평가 척도
# 1. 지지도(support) : 전체자료에서 A를 구매한 후 B를 구매하는 거래 비율 
#  A->B 지지도 식 
#  -> A와 B를 포함한 거래수 / 전체 거래수
#  -> n(A, B) : 두 항목(A,B)이 동시에 포함되는 거래수
#  -> n : 전체 거래 수

# 2. 신뢰도(confidence) : A가 포함된 거래 중에서 B를 포함한 거래의 비율(조건부 확률)
# A->B 신뢰도 식
#  -> A와 B를 포함한 거래수 / A를 포함한 거래수

# 3. 향상도(Lift) : 하위 항목들이 독립에서 얼마나 벗어나는지의 정도를 측정한 값
# 향상도 식
#  -> 신뢰도 / B가 포함될 거래율
# 분자와 분모가 동일한 경우 : Lift == 1, A와 B가 독립(상관없음)
# 분자와 분모가 동일한 경우 : Lift != 1, x와 y가 독립이 아닌 경우(상관있음)


# [실습]  트랜잭션 객체를 대상으로 연관규칙 생성 

# 단계 1 : 연관분석을 위한 패키지 설치
library(arules) #read.transactions()함수 제공

# 단계 2 : 트랜잭션(transaction) 객체 생성
setwd("c:/Rwork/Part-IV")
tran<- read.transactions("tran.txt", format="basket", sep=",")
tran

# 단계 3 : 트랜잭션 데이터 보기
inspect(tran)

# 단계 4 : 규칙(rule) 발견
rule<- apriori(tran, parameter = list(supp=0.3, conf=0.1)) # 16 rule
inspect(rule) # 규칙 보기
rule<- apriori(tran, parameter = list(supp=0.1, conf=0.1)) # 35 rule 
inspect(rule) # 규칙 보기


## 2. 트랜잭션 객체 생성 

# [실습]  single 트랜잭션 객체 생성 
stran <- read.transactions("demo_single",format="single",cols=c(1,2)) 
inspect(stran)

# [실습] 중복 트랜잭션 제거

# 단계 1 : 트랜잭션 데이터 가져오기
stran2<- read.transactions("single_format.csv", format="single", sep=",", 
                           cols=c(1,2), rm.duplicates=T)

# 단계 2 : 트랜잭션과 상품 수 확인
stran2
inspect(stran2)

# 단계 3 : 요약 통계 제공 
summary(stran2) # 248개 트랜잭션에 대한 기술통계 제공
inspect(stran2) # 트랜잭션 확인 


# [실습] 규칙 발견(생성)

# 단계 1 : 규칙 생성하기 
astran2 <- apriori(stran2) # supp=0.1, conf=0.8와 동일함 
#astran2 <- apriori(stran2, parameter = list(supp=0.1, conf=0.8))
astran2 # set of 102 rules
attributes(astran2)

# 단계 2 : 발견된 규칙 보기 
inspect(astran2)

# 단계 3 : 상위 5개 향상도 내림차순으로 정렬하여 출력 
inspect(head(sort(astran2, by="lift")))


# [실습] basket 트랜잭션 객체 생성
btran <- read.transactions("c:/Rwork/Part-IV/demo_basket",format="basket",sep=",") 
inspect(btran) # 트랜잭션 데이터 보기


## 3. 연관규칙 시각화

# [실습] Adult 데이터 셋 가져오기
data(Adult) # arules에서 제공되는 내장 데이터 로딩
str(Adult) # Formal class 'transactions' , 48842(행)
Adult

# [실습] 트랜잭션 관련 정보보기
attributes(Adult)# 트랜잭션의 변수와 범주 보기
data(AdultUCI)
str(AdultUCI) # 'data.frame':	48842 obs. of  2 variables:
names(AdultUCI)

# [실습]  Adult 데이터 셋의 요약 통계량 보기 

# 단계 1 : data.frame 형식으로 보기
adult <- as(Adult, 'data.frame')
str(adult)  
head(adult)

# 단계 2 : 요약 통계량
summary(Adult)


# [실습] 신뢰도 80%, 지지도 10% 적용된 연관규칙 발견   
ar<- apriori(Adult, parameter = list(supp=0.1, conf=0.8))

# [실습] 다양한 신뢰도와 지지도 적용  예 

# 단계 1 : 지지도를 20%로 높인 경우 1,306개 규칙 발견
ar1<- apriori(Adult, parameter = list(supp=0.2)) 

# 단계 2 : 지지도 20%, 신뢰도 95% 높인 경우 348개 규칙 발견
ar2<- apriori(Adult, parameter = list(supp=0.2, conf=0.95)) # 신뢰도 높임

# 단계 3 : 지지도 30%, 신뢰도 95% 높인 경우 124개 규칙 발견
ar3<- apriori(Adult, parameter = list(supp=0.3, conf=0.95)) # 신뢰도 높임

# 단계 4 :  지지도 35%, 신뢰도 95% 높인 경우 67 규칙 발견
ar4<- apriori(Adult, parameter = list(supp=0.35, conf=0.95)) # 신뢰도 높임

# 단계 5 :  지지도 40%, 신뢰도 95% 높인 경우 36 규칙 발견
ar5<- apriori(Adult, parameter = list(supp=0.4, conf=0.95)) # 신뢰도 높임


# [실습] 규칙 결과보기

# 단계 1 : 상위 6개 규칙 보기
inspect(head(ar5)) 

# 단계 2 :  confidence(신뢰도) 기준 내림차순 정렬 상위 6개 출력
inspect(head(sort(ar5, decreasing=T, by="confidence")))

# 단계 3 :  lift(향상도) 기준 내림차순 정렬 상위 6개 출력
inspect(head(sort(ar5, by="lift"))) 


# [실습] 연관규칙 시각화

# 단계 1 : 패키지 설치 
install.packages("arulesViz") 
library(arulesViz) 

# 단계 2 : 연관규칙 시각화
plot(ar3, method='graph', control=list (type='items'))


# [실습] Groceries 데이터 셋으로 연관분석하기

# 단계 1 :  Groceries 데이터 셋 가져오기
library(arules)
data("Groceries")  # 식료품점 데이터 로딩
str(Groceries) # Formal class 'transactions' [package "arules"] with 4 slots
Groceries

# 단계 2 : data.frame으로 형 변환
Groceries.df<- as(Groceries, "data.frame")
head(Groceries.df)

# 단계 3 : 지지도 0.001, 신뢰도 0.8 적용 규칙 발견
rules <- apriori(Groceries, parameter=list(supp=0.001, conf=0.8))
inspect(rules) 

# 단계 4 : 규칙을 구성하는 왼쪽(LHS) -> 오른쪽(RHS)의 item 빈도수 보기 
library(arulesViz)
plot(rules, method="grouped")

# [실습] 최대 길이 3이하 규칙 생성
rules <- apriori(Groceries, parameter=list(supp=0.001, conf=0.80, maxlen=3))
# writing ... [29 rule(s)] done [0.00s].
inspect(rules) # 29개 규칙

# [실습] confidence(신뢰도) 기준 내림차순으로 규칙 정렬
rules <- sort(rules, decreasing=T, by="confidence")
inspect(rules) 

# [실습] 발견된 규칙 시각화
library(arulesViz) # rules값 대상 그래프를 그리는 패키지
plot(rules, method="graph", control=list(type="items"))


# [실습] 특정 상품[item] 서브 셋 작성과 시각화

# 단계 1 : 오른쪽 item이 전지분유(whole milk)인 규칙만 서브셋으로 작성
wmilk <- subset(rules, rhs %in% 'whole milk') # lhs : 왼쪽 item
wmilk # set of 18 rules 
inspect(wmilk)
plot(wmilk, method="graph") #  연관 네트워크 그래프

# 단계 2 : 오른쪽 item이 other vegetables인 규칙만 서브셋으로 작성
oveg <- subset(rules, rhs %in% 'other vegetables') # lhs : 왼쪽 item
oveg # set of 10 rules 
inspect(oveg)
plot(oveg, method="graph") #  연관 네트워크 그래프

# 단계 3 :  오른쪽 item이 vegetables 단어가 포함된 규칙만 서브 셋으로 작성
veg <- subset(rules, rhs %pin% 'vegetables') 
veg 
inspect(oveg)

# 단계 4 : 왼쪽 item이 butter or yogurt인 규칙만 서브 셋으로 작성
butter_yog <- subset(rules, lhs %in% c('butter', 'yogurt'))
butter_yog
inspect(butter_yog)
plot(butter_yog, method="graph")
