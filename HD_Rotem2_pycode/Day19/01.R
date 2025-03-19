#변량에 준하는 estimate값이0이다다 

data(ChickWeight)
str(ChickWeight)
m <- lm(weight ~ Time, data = ChickWeight)
summary(m)

with(ChickWeight, plot(Time, weight))

par(mfrow = c(2,2))
plot(m)

install.packages("car")
library(car)
m2 <- lm(Sepal.Length~., data = iris)
vifresult <- car::vif(m2)
summary(vifresult)
vifresult
