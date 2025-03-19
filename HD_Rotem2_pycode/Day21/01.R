raw_data <- read.csv("binary.csv", encoding = "cp949")

head(raw_data)
nrow(raw_data)
plot(raw_data)

m2 <- glm(admit ~ gre, data=raw_data, family = binomial(link="probit"))

summary(m2)

probit_admit <- glm(admit ~ gre + gpa + rank, data = raw_data,
                    family = binomial(link = "probit"))
probit_admit
summary(probit_admit)
coef(probit_admit)

exp(coef(probit_admit))
