data()  #iris datasets을 사용용

str(iris)
# 회귀변수의 y값은 연속형 데이터여야한다
summary(iris)

SepalLength <- iris$Sepal.Length
SepalWidth <- iris$Sepal.Width
PetalLength <- iris$Petal.Length
PetalWidth <- iris$Petal.Width

#Sepal.Length와 Sepal.Width의 상관관계 분석
cov(SepalLength, SepalWidth)
cor(SepalLength, SepalWidth)
cor.test(SepalLength, SepalWidth, conf.level = 0.95)

plot(SepalLength, SepalWidth, col = iris$Species)

#Sepal.Length
cov(SepalLength, PetalWidth)
cor(SepalLength, PetalWidth)
cor.test(SepalLength, PetalWidth, conf.level = 0.95)

plot(SepalLength, PetalWidth, col = iris$Species)

cov(SepalLength, PetalLength)
cor(SepalLength, PetalLength)
cor.test(SepalLength, PetalLength, conf.level = 0.95)

plot(SepalLength, PetalLength, col = iris$Species)

# boxplot을 위한 데이터 프레임 생성
data <- data.frame(SepalLength, SepalWidth, PetalLength, PetalWidth)

# boxplot 생성
boxplot(data, names = c("SepalLength", "SepalWidth", "PetalLength", "PetalWidth"))

pairs(~ Sepal.Width + Sepal.Length + Petal.Width + 
        Petal.Length, data = iris, col = iris$Species)

#회귀분석- 선형성 파악() : Sepal.Length(꽃받침의 길이)
#install.packages("psych")
library(psych)
corr.test(iris[-5])

#install.packages("corrgram")
library(corrgram)
corrgram(iris[-5])

#install.packages("PerformanceAnalytics")
library(PerformanceAnalytics)
chart.Correlation(iris[-5], histogram = ,pch="+")

hist(iris$Sepal.Length)

result <- lm(Sepal.Length ~ Sepal.Width + Petal.Length + Petal.Width, data = iris)
result

lm(result)
summary(lm(result))
