data(iris)
idx<-sample(1:nrow(iris),40)
irisSample<-iris[idx,]
irisSample$Species<-NULL
str(irisSample)

hc<-hclust(dist(irisSample), method="average")
plot(hc, hang=-1, labels=iris$Species[idx])
rect.hclust(hc, h=3)
#각데이터가 속한 클러스터 확인
group <-cutree(hc, k=3)
group
