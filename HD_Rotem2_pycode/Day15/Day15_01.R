# H0 : 만족 인원(1)은 전체 인원의 80%이다
# H1 : 만족 인원(1)은 전체 인원의 80%이 아니다
data <- read.csv("one_sample.csv", header = TRUE)
x <- data$survey
summary(x)

length(x)
table(x) #모든 함수는 1을 기준으로 계산한다. 반드시 기억할 것

install.packages("prettyR")
library(prettyR) #freq 함수 사용

freq(x)
x[x == 1] <- "만족"
x[x == 0] <- "불만족"
table(x)

#검사의 신뢰도를 위해 항상 양측검정과 단측검정을 동시에 실행해야한다. 
binom.test(c(136,14), p = 0.8)
binom.test(c(136,14), p = 0.8, alternative = "two.sided", conf.level = 0.95)
binom.test(c(136,14), p = 0.8, alternative = "greater", conf.level = 0.95)
binom.test(c(136,14), p = 0.8, alternative = "less", conf.level = 0.95)