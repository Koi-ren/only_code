#H0 : 광고 매체와 매출액은 인과관계가 없다
#H1 : 광고 매체와 매출액은 인과관계가 있다

sale_data <- read.csv("advertising.csv")

head(sale_data)
summary(sale_data) #결측치 없음
hist(sale_data$Sales) #판매량은 정규성을 따른다

#독립변수가 두개 이상임으로 중회귀

#각 독립변수가 서로상관관계에 있는지 우선적으로 확인
library(psych)
library(corrgram)
library(PerformanceAnalytics)
corr.test(sale_data)
corrgram(sale_data)
plot(sale_data, col = 5)
par(mfrow = c(2,2))
qqplot(sale_data$Sales, sale_data$TV)
qqplot(sale_data$Sales, sale_data$Radio)
qqplot(sale_data$Sales, sale_data$Newspaper)

plot(sale_data$TV, sale_data$Sales)
abline(lm(Sales ~ TV, data = sale_data), col = "red")
plot(sale_data$Radio, sale_data$Sales)
abline(lm(Sales ~ Radio, data = sale_data), col = "red")
plot(sale_data$Newspaper, sale_data$Sales)
abline(lm(Sales ~ Newspaper, data = sale_data), col = "red")

chart.Correlation(sale_data, histogram = ,pch="+")

result <- lm(Sales ~ TV + Radio + Newspaper, data = sale_data)
summary(result)

par(mfrow = c(2,2))
plot(result)