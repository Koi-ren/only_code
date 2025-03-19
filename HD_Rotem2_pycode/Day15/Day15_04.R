# H0 : 대학생의 진학 대학에 대한 만족도 차이는 성별로 차이가 없다
# H1 : 대학생의 진학 대학에 대한 만족도 차이는 성별로 차이가 있다

data <- read.csv("two_sample.csv")
head(data)
summary(data)

gender <- data$gender
survey <- data$survey

gender[data$gender == 1] <- "남자"
gender[data$gender == 2] <- "여자"
survey[data$survey == 0] <- "반대"
survey[data$survey == 1] <- "찬성"

table(gender, survey)

prop.test(c(36,19), c(174, 126), conf.level = 0.95)
prop.test(c(36,19), c(174, 126), alternative = "greater", conf.level = 0.95)
prop.test(c(36,19), c(174, 126), alternative = "less",conf.level = 0.95)
