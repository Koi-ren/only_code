data(cars)
cars
m <- lm(dist ~speed, cars) #dist = 독립변수, speed = 종속변수 
summary(m)

par(mfrow=c(2,2))
plot(m)


