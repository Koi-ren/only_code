getwd()

setwd("c:/ws/HD_Rotem2_pycode/Day13")
data <- read.csv("paired_sample.csv", header = TRUE)
data
summary(data)
#after에서 NA값 4개 검출, 전처리 필요

result <- subset(data, !is.na(after), c(before, after))

result
summary(result)

x <- result$before
y <- result$after

x; y

length(x)
length(y)
mean(x)
mean(y)

var.test(x, y, paired = TRUE)
#p-value는 0.7361로 0.05보다 큼, 따라서 분포형태 동질함

t.test(x, y, paired = TRUE) #기본은 two.sided임
t.test(x, y, paired = TRUE, alter = "two.sided", conf.int = TRUE, conf.level = 0.95)

t.test(x, y, paired=TRUE,alter="greater",conf.int=TRUE, conf.level=0.95)

t.test(x, y, paired=TRUE,alter="less",conf.int=TRUE, conf.level=0.95)
