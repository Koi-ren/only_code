x <- c(19,23, 26,29,30, 38, 39, 46, 49)
y <- c(33, 51, 40, 49, 50, 69, 70, 64, 89)

shapiro.test(x)
shapiro.test(y)
#x와 y가 정규분포함 

par(mfrow = c(2,2))
plot(x, y, xlab = "예약대수", ylab = "판매대수")
boxplot(x,y, names = c("예약대수", "판매대수"))
barplot(y, names.arg = x, xlab = "예약대수", ylab = "판매대수")

cov(x, y)
cor(x, y)
cor.test(x, y, conf.level = 0.95)

lm(formula = y ~ x)
m <- lm(formula = y ~ x)
summary(m)
shapiro.test(m$residuals)

par(mfrow = c(1,1))
plot(m$residuals ~ m$fitted.values, xlab = "예측 값", ylab = "잔차")
abline(h = 0, col = "red")

par(mfrow = c(2,2))
plot(m)
