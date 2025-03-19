install.packages("ggplot2")

###---동일한 타입(수학 데이터)
x <- 30
x1 <- c(10,20,30,40,50) #vector
x1[1]
x2 <- matrix(data = c(10, 20, 30, 40, 50, 60), nrow=2) #matrix(2 --> (2, 3)) 차원 별로 명령어가 다름
x2 #정형 구조만 만질 수 있고, 또한 수학 모델만 만들 수 있음
x2[2,3] #행렬의 2행 3열
x2[2][3] #벡터의 3번째 원소 ==> 비정상적인 접근임
x2[,c(1,3)] #행렬의 1,3열을 묶어서 차원을 줄이자!

#---다양한 Data type 다루기
num <- seq(from = 1, to = 10, by = 2) #1부터 10까지 2씩 증가
cha <- rep(x = c('a','b'), each=3)

lst1 <- list(num)
#lst1 <- list(c(num, cha))
lst1
lst2 <- list(c(1,10.5,'hello'))
lst2
lst3 <- list(a = num, b = cha)
lst3
class(lst1)
str(lst1)
lst3$a
lst3$b

num <- seq(from = 1, to = 6, by = 1) #1부터 10까지 2씩 증가
cha <- rep(x = c('a','b'), each=3)

df <- data.frame(num, cha) #데이터 차수가 다르기에 생성 불가 가능
df
num