getwd()
data <- read.csv("one_sample.csv", header = TRUE)
data
head(data)

#H0: 양치기 개의 평균 심장 박동수 모평균 = 115
#H1: 모평균은 115가 아니다.

sample <- c(93, 109, 110, 89, 112, 117)
#평균 = 0, 편차 = 1
#H0
shapiro.test(sample)
#p-value는 이 샘플 데이터가 모집단의 귀무가설을 지지하는 확률임
#(지지율이5%이하로 떨어지면 귀무가설을 더이상 지지하지 않는다는 의미)
#이 코드에서는 샘플이 귀무가설을 20%정도의 지지율을 의미함

'''
실행결과

	Shapiro-Wilk normality test

data:  sample
W = 0.8655, p-value = 0.2089
'''

hist(sample)
qqnorm(sample)
qqline(sample, lty = 1, col = 'red')

#내가 검증하고 싶은거는 sample데이터이고 모평균은 115이다 이를 확인해달라
#ㄴ--> t.test(sample, mu = 115)

t.test(sample, mu = 115)

#실행 결과

#data:  sample
#t = -2.1753, df = 5, p-value = 0.0816
#alternative hypothesis: true mean is not equal to 115
#95 percent confidence interval:
#  93.18278 116.81722
#sample estimates:
#mean of x 

#만약 귀무가설이 틀렸다면 모수는 틀렸다는 뜻임
#sample은 정상적이라고 가정한다
