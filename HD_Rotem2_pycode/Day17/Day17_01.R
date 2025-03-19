data(iris)
m <- lm(formula = Sepal.Length ~ Sepal.Width + Petal.Length + Petal.Width, data = iris)
summary(m)

m2 <- lm(Sepal.Length ~. , data = iris)
summary(m2)
#여기서는 virsinica와 setosa, versicolor 같은 꽃의종류가 숫자로 구분된다.
#이를 막기 위해 벡터라이징을 한다. ==> 더미 변수를 만들어서..

model.matrix(m2)[c(1,51,101),]
#여기서 보면 품종별로 하나씩만 샘플로 보아 확인할 수 있으며
#이때 Speciesvesicolor, Speciesviginica에서 더미변수 두개로 표현된 벡터라이징을 확인할 수있다. 

model.matrix(m)[c(1,51,101),]

with(iris, plot(Sepal.Width, Sepal.Length, cex =.7, pch = as.numeric(Species)))

as.numeric(iris$Species)

m <- lm(Sepal.Length ~ Sepal.Width + Species, data=iris)
coef(m)

abline(2.25, 0.80, lty=1)
abline(2.25 + 1.45, 0.80, lty=2)
abline(2.25 + 1.94, 0.80, lty=3)

legend("topright", levels(iris$Species), pch=1:3, bg="white")

levels(iris$Species)

#회귀식이 범주형에도 적용될수 있다.
#회귀식 자체는 수치 예측용으로 쓰인다
#정확도는 떨어질수 있다
#따라서 회귀식 자체는 y값이 주어지면 y에 영향을 주는 것이 무엇이 있는지 찾아
#예측의 정확도를 높이는 것을 목표로하는 것이 좋다.

#y가 양적데이터인지, 질적데이터인지에 따라서 알고리즘이 다르다.
#회귀식 자체는 모형을 예측하는 모형으로서 현실에서 잘 쓰이진 않지만
#머신러닝을 포함한 딥러닝까지 모든 것의 학술적인 기본에 해당하는 것이기에 
#반드시 알아야하지만 여러 가치면에서도 효율성은 존재한다

#데이처 수집전처리 과정을 거치고,
#모델링을 한 후 평가를 한다면(가장 기본의 4단계 프로세스)

#일단 클리닝 작업(전처리 프로세싱)부터 한다.
#필요로하는 목표 독립변수를 걸러내는 것을 의미한다. -> 이를 변수선별이라고 한다.
#즉 y값에 영향을 끼치는 변량이 무엇인가를 정하는 것이며,
#이의 진위여부는 아직 알수 없다.

