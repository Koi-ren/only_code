# chap15_4_2_RandomForest

######################################
## Chapter15_4_2. RandomForest
######################################
# 결정트리(Decision tree)에서 파생된 모델 
# 랜덤포레스트는 앙상블 학습기법을 사용한 모델
# 앙상블 학습 : 새로운 데이터에 대해서 여러 개의 Tree로 학습한 다음, 
# 학습 결과들을 종합해서 예측하는 모델(PPT 참고)
# DT보다 성능 향상, 과적합 문제를 해결


# 랜덤포레스트 구성방법(2가지)
# 1. 결정 트리를 만들 때 데이터의 일부만을 복원 추출하여 트리 생성 
#  -> 데이터 일부만을 사용해 포레스트 구성 
# 2. 트리의 자식 노드를 나눌때 일부 변수만 적용하여 노드 분류
#  -> 변수 일부만을 사용해 포레스트 구성 
# 새로운 데이터 예측 방법
# - 여러 개의 결정트리가 내놓은 예측 결과를 투표방식(voting) 방식으로 선택 


## [실습] 랜덤 포레스트 기본 모델 생성  

# 단계1 : 패키지 설치 및 데이터 셋 가져오기
#install.packages('randomForest')
library(randomForest) # randomForest()함수 제공 
data(iris)

# 단계2 :  랜덤 포레스트 모델 생성 
# 형식) randomForest(y ~ x, data, ntree, mtry)
model = randomForest(Species~., data=iris)  
model


## [실습] 파라미터 조정 300개의 Tree와 4개의 변수 적용 모델 생성 
model2 = randomForest(Species~., data=iris, 
                     ntree=300, mtry=4, na.action=na.omit )
model2


## [실습] 중요 변수 생성으로 랜덤 포레스트 모델 생성 

# 단계1 :  중요 변수로 랜덤 포레스트 모델 생성  
model3 = randomForest(Species ~ ., data=iris, 
                      ntree=500, mtry=2, 
                      importance = T,
                      na.action=na.omit )
model3 

# 단계2 :  중요 변수 보기
importance(model3)

# 단계3 :  중요 변수 시각화
varImpPlot(model3)

## [실습] 파라미터 조정 : 트리 개수 300개, 변수 개수 4개 지정 

# 단계1 : 속성값 생성 
ntree <- c(400, 500, 600)
mtry <- c(2:4)

# 2개 vector이용 data frame 생성 
param <- data.frame(n=ntree, m=mtry)
param

# 단계2 : 이중 for 함수 이용 모델 생성 
for(i in param$n){ # 400,500,600
  cat('ntree = ', i, '\n')
  for(j in param$m){ # 2,3,4
    cat('mtry = ', j, '\n')
    model_iris = randomForest(Species~., data=iris, 
                         ntree=i, mtry=j, 
                         na.action=na.omit )
    print(model_iris)
  }
}
