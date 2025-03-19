#install.packages("mlbench")
library(mlbench)
data(BostonHousing)
str(BostonHousing)
help("BostonHousing")

m <- lm(medv ~ . , data = BostonHousing)
m_step <- step(m, direciton = "both")
#모든 조합에 대한 회귀식평가
#install.packages("leaps")
library(leaps)

all_m <- regsubsets(medv~ . , data = BostonHousing)
sm <- summary(all_m)
sm$bic
sm$adjr2

plot(all_m, scale="adjr2")