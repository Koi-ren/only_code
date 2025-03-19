getwd()
setwd("c:/ws/HD_Rotem2_pycode/Day14")
data <- read.csv("cleanDescriptive.csv", header = TRUE, fileEncoding = "cp949")

x <- data$level2
y <- data$pass2

summary(x)
x1 <- as.factor(x)
summary(x1)
summary(x)

table(x)

#교차분석 --> 카이제곱분포를따르는지를 확인
# ==> 기대치와 관측치의 차이가 없다
result <- data.frame(Level = x, Pass = y)
head(result)

table(result)

###install.packages("gmodels")
library(gmodels)  #crossTable()
###install.packages("ggplot2")
library(ggplot2)

CrossTable(x,y, chisq = TRUE)
