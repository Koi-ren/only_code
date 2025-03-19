data <- read.csv("smoke.csv", header = TRUE)
head(data)
table(data)
summary(data)

library(gmodels)

x <- data$education
y <- data$smoking

data$education_mapping[data$education == 1] <- "대졸"
data$education_mapping[data$education == 2] <- "고졸"
data$education_mapping[data$education == 3] <- "중졸"

data$smoking_mapping[data$smoking == 1] <- "과다흡연"
data$smoking_mapping[data$smoking == 2] <- "보통흡연"
data$smoking_mapping[data$smoking == 3] <- "비흡연"

new_table <- table(data$education_mapping, data$smoking_mapping)

cross_table <- new_table
CrossTable(data$education_mapping, data$smoking_mapping, chisq = TRUE)

barplot(new_table,beside = F,legend = row.names(new_table), col = c("red", "green", "blue"), xlab = "흡연율",ylab = "인수")
barplot(prop.table(cross_table, margin = 1.3), beside = FALSE, col = c("red", "green", "blue"),legend = rownames(cross_table), main = "교육수준별 흡연율", xlab = "흡연율",ylab = "비율")
