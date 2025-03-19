data <- read.csv("three_sample.csv", header = TRUE)
head(data)

method <- data$method #교육방법
survey <- data$survey #만족도

method; survey

table(method, useNA = 'ifany')
table(method, survey, useNA = 'ifany')

prop.test(c(34, 37, 39), c(50, 50, 50))
prop.test(c(34, 37, 39), c(50, 50, 50), alter = "two.sided", conf.level = 0.95)

