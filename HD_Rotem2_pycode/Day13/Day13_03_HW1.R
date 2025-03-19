getwd()
setwd("c:/ws/HD_ROtem2_pycode/Day13")
data <- read.csv("two_sample.csv", header = TRUE)
data
head(data)

summary(data)
#결측치 == 73개, 데이터 전처리 필요

result <- subset(data, !is.na(score), c(method, score))
length(result$score)

result

a <- subset(result, method == 1)
b <- subset(result, method == 2)

a1 <- a$score
b1 <- b$score

length(a1)
length(b1)
mean(a1)
mean(b1)

var.test(a1, b1)

t.test(a1, b1)

t.test(a1, b1, alter = "two.sided", conf.int = TRUE, conf.level = 0.95)

t.test(a1, b1, alter = "less", conf.int = TRUE, conf.level = 0.95)

t.test(a1, b1, alter = "greater", conf.int = TRUE, conf.level = 0.95)

