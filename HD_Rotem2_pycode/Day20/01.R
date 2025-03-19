data(iris)
?head
head(iris)

d <- subset(iris, Species == "virginica" | Species == "versicolor" )

str(d)
d$Species <- factor(d$Species)
str(d)

#logistic Regreesion
m <- glm(Species ~ ., data=d, family="binomial")
m
predict(m, newdata=d[c(1,10,55),], type="response")
