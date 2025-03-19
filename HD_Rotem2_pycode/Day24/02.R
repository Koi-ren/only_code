#install.packages("TTR")
install.packages("forecast")
library(TTR)
library(forecast)
kings<-scan("http://robjhyndman.com/tsdldata/misc/kings.dat", skip=3)
head(kings)
kings_ts<-ts(kings)
kings_ts
plot.ts(kings_ts)

kings_d1 <- diff(kings_ts, differences = 1)
kings_d2 <- diff(kings_ts, differences = 2)
kings_d3 <- diff(kings_ts, differences = 3)


par(mfrow=c(2,2))
plot.ts(kings_ts)
plot.ts(kings_d1)
plot.ts(kings_d2)
plot.ts(kings_d3)

kings_sma <- SMA(kings_ts, n=3)
kings_sma_d1 <- SMA(kings_d1, n=3)

#install.packages("tseries")
library(tseries)
kp.test(kings_d1)

par(mfrow=c(1,2))
plot.ts(kings_sma)
plot.ts(kings_sma_d1)

acf(kings_d1, lag.max = 20) #MA(1)
pacf(kings_d1, lag.max = 20) #AR

auto.arima(kings) #MA(1) c(0, 1, 1)

my_kings_arima <- arima(kings_ts, order = c(2, 1, 1))
auto_kings_arima <- arima(kings_ts, order= c(0, 1, 1))

forecast(my_kings_arima, h = 5)
forecast(auto_kings_arima, h = 5)