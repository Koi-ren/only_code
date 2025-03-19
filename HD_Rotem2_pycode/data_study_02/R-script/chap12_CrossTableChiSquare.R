# chap12_CrossTableChiSquare 

########################################
## Chapter12. 교차분석과 카이제곱검정 
########################################

## 1. 교차분석

# 1.1 데이터프레임 생성 

# [실습] 변수 리코딩과 데이터프레임 생성 
#  1)  실습파일 가져오기
setwd("c:/Rwork/Part-III")
data <- read.csv("cleanDescriptive.csv", header=TRUE)
data # 확인
head(data) # 변수 확인

# 2) 변수 리코딩 
x <- data$level2 # 리코딩 변수 이용
y <- data$pass2 # 리코딩 변수 이용
x; y # 부모학력수준(x) -> 자녀대학진학여부(y) 

# 3) 데이터프레임 생성 
result <- data.frame(Level=x, Pass=y) # 데이터 프레임 생성 - 데이터 묶음
dim(result) # 차원보기
head(result)


# 1.2 교차분석 

# 1) 교차분할표 작성   
table(result) # 빈도보기

# 2) 교차 분할표 생성을 위한 패키지 설치
install.packages("gmodels") # gmodels 패키지 설치
library(gmodels) # CrossTable() 함수 사용
install.packages("ggplot2") # diamonds 데이터 셋 사용을 위한 패키지 설치
library(ggplot2)

# 3) 패키지를 이용한 교차 분할표 생성
CrossTable(x=diamonds$color, y=diamonds$cut) 


# [실습] 패키지를 이용한 부모 학력 수준과 자녀 대학진학 여부 교차 분할표 작성 
x <- data$level2
y <- data$pass2
CrossTable(x, y)

# 교차테이블에 카이검정 적용 
CrossTable(x, y, chisq = T)


##  2. 카이제곱 검정 

# 1) 일원카이제곱 

# (1) 적합성 검정 예
#-----------------------------------------------
# 귀무가설 : 기대치와 관찰치는 차이가 없다.  : p >= 알파 
#     예) 주사위는 게임에 적합하다.
# 대립가설 : 기대치와 관찰치는 차이가 있다.   : p < 알파 
#     예) 주사위는 게임에 적합하지 않다.
#-----------------------------------------------

# 60회 주사위를 던져서 나온 관측도수/기대도수
# 관측도수 : 4, 6, 17,16 ,8,9
# 기대도수 : 10,10,10,10,10,10

chisq.test(c(4,6,17,16,8,9))

# (2) 선호도 분석 
#-----------------------------------------
# 귀무가설 : 기대치와 관찰치는 차이가 없다. 
#       예) 스포츠음료의 선호도에 차이가 없다.
# 대립가설 : 기대치와 관찰치는 차이가 있다. 
#       예) 스포츠음료의 선호도에 차이가 있다.
#-----------------------------------------
data <- textConnection(
  "스포츠음료종류  관측도수
  1   41
  2   30
  3   51
  4   71
  5   61
  ")
x <- read.table(data, header=T)
x # 스포츠음료종류 관측도수

chisq.test(x$관측도수)


# 2) 이원카이제곱 - 교차분할표 이용

# (1) 독립성

# •연구가설(H1)	:	부모의	학력	수준과	자녀의	대학진학	여부는	관련성이	있다.		
# •귀무가설(H0)	:	부모의	학력	수준과	자녀의	대학진학	여부는	관련성이	없다.	

# 독립변수(x)=설명변수, 종속변수(y)=반응변수 생성 
data <- read.csv("cleanDescriptive.csv", header=TRUE)
x <- data$level2 # 부모의 학력수준
y <- data$pass2 # 자녀의 대학진학여부 

CrossTable(x, y, chisq = TRUE) #p =  0.2507057    


# (2) 동질성 검정 
# 귀무가설 : 교육방법에 따라 만족도에 차이가 없다.
# 대립가설 : 교육방법에 따라 만족도에 차이가 있다.


# 1. 파일 가져오기
setwd("c:/Rwork/Part-III")
data <- read.csv("homogenity.csv", header=TRUE)
head(data) 
# method와 survery 변수만 서브셋 생성
data <- subset(data, !is.na(survey), c(method, survey)) 
data

# 2. 변수리코딩 - 코딩 변경

# 교육방법2 필드 추가
data$method2[data$method==1] <- "방법1" 
data$method2[data$method==2] <- "방법2"
data$method2[data$method==3] <- "방법3"

# 만족도2 필드 추가
data$survey2[data$survey==1] <- "1.매우만족"
data$survey2[data$survey==2] <- "2.만족"
data$survey2[data$survey==3] <- "3.보통"
data$survey2[data$survey==4] <- "4.불만족"
data$survey2[data$survey==5] <- "5.매우불만족"

# 3. 교차분할표 작성 
table(data$method2, data$survey2)  # 교차표 생성 -> table(행,열)

# 4. 동질성 검정 - 모수 특성치에 대한 추론검정  
chisq.test(data$method2, data$survey2) 


# 5. 동질성 검정 해석
# 교육방법에 따른 집단 간의 만족도에 차이가 없다.

