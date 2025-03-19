# #H0: 스프레이 종류에 따른 살충효과의 차이가 없다
# #H0: 스프레이 종류에 따른 살충효과의 차이가 있다
# 
# data("InsectSprays")
# 
# summary(InsectSprays)
# #결측치 없음
# 
# head(InsectSprays)ㅁ
# 
# table(InsectSprays$spray)
# xtabs(~ count + spray, data = InsectSprays)
# 
# boxplot(count ~ spray, data = InsectSprays,
#         main = "Insect Counts vs Spray Type",
#         xlab = "Spray", ylab = "Count")
# 
# m <- lm(count ~. , data = InsectSprays)
# m
# summary(m)
# 
# all_m <- regsubsets(count ~. , data=InsectSprays)
# sm <- summary(all_m)
# sm$bic
# sm$adjr2
# plot(all_m, scale="adjr2")
# 
# par(mfrow = c(2,2))
# plot(m)


#---------------교수님 풀이----------------
str(InsectSprays)
sprays.lm <- lm(formula = count ~ spray, data = InsectSprays)
summary(sprays.lm)

contrasts(InsectSprays$spray)
summary(sprays.lm)

F <- aov(count ~ spray, data = InsectSprays)
summary(F)
TukeyHSD(F)
