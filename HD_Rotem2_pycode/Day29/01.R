data("USArrests")

str(USArrests)

head(USArrests)

colnames(USArrests)

rownames(USArrests)

#dist함수로 인스턴스간 거리 계산(유클리드 거리)

d<-dist(USArrests,method="euclidean")

#method can be one of ward.D,complete,median ...

fit<-hclust(d,method="ave") #평균연결법

fit

plot(fit,cex=0.6)
plot(fit,hang=-1,cex=0.6) #hang은 레이블이 나머지 플롯 아래에 있어야하는 플롯 높이의 비율 (음수 지정시 레이블이 0에서 중단 )
rect.hclust(fit,k=6,border="red")
rect.hclust(fit,k=3,border="blue")
#계층적군집의 결과로 k는 그룹수 h는 높이



par(mfrow=c(1,1))

groups<-cutree(fit,k=6)

treeheights=cutree(fit,h=30)

plot(fit)

rect.hclust(fit,k=6,border="red")

hca<-hclust(dist(USArrests))

plot(hca)

rect.hclust(hca, k = 3, border = "red")

rect.hclust(hca, h=30, which = c(2,7), border=3:4)

hcd <- as.dendrogram(fit) 

plot(hcd, type = "rectangle", ylab = "Height") # Default plot

plot(hcd, type = "triangle", ylab = "Height") # Triangle plot

#노드파라미스트를 리스트로 만들어 노드에 대한 옵션 설정 가능

nodePar <- list(lab.cex = 0.6, pch = c(NA,19), cex = 0.7, col = "blue") # Define nodePar

plot(hcd, ylab = "Height", nodePar = nodePar, leaflab = "none") # Customized plot; remove labels

plot(hcd, xlab = "Height", nodePar = nodePar, horiz = TRUE) # Horizontal plot

#노드에 잇는 선에 대한 옵션이랄까?

edgePar = list(col = 2:3, lwd = c(10,3))

plot(hcd, ylab = "Height", nodePar = nodePar, edgePar = edgePar)

#agines->병합적 방법, 작은 군집에서 큰 군집으로 군집해가는 방식

library(cluster)

agn1<-agnes(USArrests,metric="manhattan",stand=TRUE) #metric으로 거리계산법 지정(맨하튼)

agn1

par(mfrow=c(1,2))

plot(agn1)

agn2 <- agnes(daisy(USArrests), diss=TRUE, method = "complete") #daisy() 함수는 데이터 관측치 사이의 거리를 계산해 주며, 자료의 형태가 수치형일 필요가 없다는 점에서 dist() 함수보다 유연하다.

plot(agn2)

agn3 <- agnes(USArrests, method="flexible", par.meth = 0.3) 

plot(agn3) 
