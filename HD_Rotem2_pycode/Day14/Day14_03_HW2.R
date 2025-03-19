getwd()
data <- read.csv("cleanData.csv", header = TRUE, fileEncoding = "cp949")

head(data)

data$position_1[data$position == 1] <- "사원"
data$position_1[data$position == 2] <- "과장"
data$position_1[data$position == 3] <- "차장"
data$position_1[data$position == 4] <- "부장"
data$position_1[data$position == 5] <- "국장"
data$age3_1[data$age3 == 1] <- "50"
data$age3_1[data$age3 == 2] <- "40대"
data$age3_1[data$age3 == 3] <- "2~30대"

table_new <- table(data$position_1, data$age3_1)
table_new
barplot(table_new,beside = F,legend = row.names(table_new), col = c("red", "green", "blue","yellow","black"), xlab = "age",ylab = "position")

library(gmodels)
CrossTable(data$position_1, data$age3_1, chisq = TRUE)