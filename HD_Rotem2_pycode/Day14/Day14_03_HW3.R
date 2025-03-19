data <- read.csv("response.csv", header = TRUE)
head(data)
summary(data) #질적데이터, 결측치 없음

job <- data$job
response <- data$response

job[job == 1] <- "학생"
job[job == 2] <- "직장인"
job[job == 3] <- "주부"

response[response == 1] <- "무응답"
response[response == 2] <- "낮음"
response[response == 3] <- "높음"

table(job, response)

job <- as.factor(job) 
response <- as.factor(response)

library(gmodels)
library(ggplot2)

ggplot(data, aes(x = job, fill = response, group = response)) +
  geom_bar(position = 'dodge') + coord_flip()

CrossTable(job, response, chisq = TRUE)
chisq.test(job, response)
