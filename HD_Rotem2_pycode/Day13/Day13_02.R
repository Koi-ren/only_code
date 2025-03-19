str(data)
x <- data$time
head(x)

#결측치의 개수를 세는 법: summary(x)
summary(x)

#그냥 평균 구하기: mean(x)
mean(x)

# 결측치를 제외한 평균을 구하는 첫번째 방법: mean(x, na.rm = T)
mean(x, na.rm = T)
# 결측치를 제외한 평균을 구하는 두번째 방법: x1 <- na.omit(x)
x1 <- na.omit(x)

mean(x1)

hist(x1)
qqnorm(x1)
qqline(x1, col = 'blue')

#함수 형식 보기: help(t.test) (Ex: t.test {stats})
help(t.test)

t.test(x1, mu = 5.2)
#t.test(x1, mu = 5.2, alternative = c("two.side"), conf.level = 0.95)로도 표현 가능함
t.test(x1, mu = 5.2, alter = "two.side", conf.level = 0.95)

#표본검정(표본1, 표본2 - 대응, 독립)
#H0: mu = 5.2
#H1: mu < 5.2  <-- 단측 검정(alternative = c("less")) 시행 시

t.test(x1, mu = 5.2, alternative = c("less"))
#H0: mu = 5.2
#H1: mu > 5.2 <-- 단측 검정(alternative = c("greater")) 시행 시
t.test(x1, mu = 5.2, alternative = c("greater"))

#옛날에는 됐는데 요즘엔 안됨:  t.test(x1, mu = 5.2, alternative = c("two.side", "less", "greater")

result <- t.test(x1, mu = 5.2, alter = "greater", conf.level = 0.95)
names(result)
