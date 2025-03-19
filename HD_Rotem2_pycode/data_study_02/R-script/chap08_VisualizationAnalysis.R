#chap08_VisualizationAnalysis

#####################################
## Chapter08. 고급시각화 분석 
#####################################

## 2. 격자형 기법 시각화

# [실습] 패키지 설치와 실습 데이터 셋 가져오기 
install.packages("lattice")
library(lattice)

install.packages("mlmRev")
library(mlmRev)
data(Chem97)

str(Chem97) # data.frame':  31022 obs. of  8 variables:
table(Chem97$score)

head(Chem97,30) # 앞쪽 30개 레코드 

# 2.1 히스토그램 
histogram( ~ gcsescore, data=Chem97) 
# gcsescore변수를 대상으로 백분율 적용 히스토그램

histogram # histogram(~x축 | 조건, dataframe)
table(Chem97$score) #  0  2  4   6  8  10 <- 빈도수
# score 변수를 조건으로 지정 
histogram(~gcsescore | score, data=Chem97) # score 단위 
histogram(~gcsescore | factor(score), data=Chem97) # score 요인 단위

# 2.2 밀도 그래프 
densityplot(~gcsescore | factor(score), data=Chem97, 
            groups = gender, plot.points=T, auto.key = T) 
# 밀도 점 : plot.points=F
# 범례: auto.key=T
# 성별 단위(그룹화)로 GCSE점수를 밀도로 플로팅    


# 2.3 막대 그래프 

# 1) 데이터셋 가져오기
data(VADeaths)
VADeaths
str(VADeaths)

# 2) 데이터셋 구조보기
mode(VADeaths) # numeric
class(VADeaths) # matrix

# 3) 데이터 리모델링
# (1) matrix -> data.frame 변환
df <- as.data.frame(VADeaths)
str(df) # 'data.frame':	5 obs. of  4 variables:
class(df) # "data.frame"
df 

# (2) matrix -> data.table 변환
dft <- as.data.frame.table(VADeaths)
str(dft) # 'data.frame':  20 obs. of  3 variables:
class(dft) # "data.frame"
dft # Var1  Var2 Freq -> 1열 기준으로 data.table 생성

# [실습] 막대 그래프 그리기 
barchart(Var1 ~ Freq | Var2, data=dft, layout=c(4,1))
# Var2변수 단위(그룹화)로 x축-Freq, y축-Var1으로 막대차트 플로팅

# [실습] 막대 그래프 그리기(origin 속성 사용)
barchart(Var1 ~ Freq | Var2, data=dft, layout=c(4,1), origin=0)


# 2.4 점 그래프 
dotplot(Var1 ~ Freq | Var2 , dft) 

dotplot(Var1 ~ Freq | Var2 , dft, layout=c(4,1)) 

# [실습] Var2변수 단위로 그룹화하여 점을 연결하여 플로팅  
dotplot(Var1 ~ Freq, data=dft, groups=Var2, type="o", 
        auto.key=list(space="right", points=T, lines=T)) 


# 2.5 산점도 그래프 
library(datasets)
str(airquality) # datasets의 airqulity 테이터셋 로드

airquality # Ozone Solar.R Wind Temp Month(5~9) Day

# airquality의 Ozone(y),Wind(x) 산점도 플로팅
xyplot(Ozone ~ Wind, data=airquality) 
range(airquality$Ozone,na.rm=T)
xyplot(Ozone ~ Wind | Month, data=airquality) # 2행3컬럼 
xyplot(Ozone ~ Wind | factor(Month), data=airquality, layout=c(5,1))

# [실습] airquality 데이터셋의 Month 타입변경(factor)
convert <- transform(airquality, Month=factor(Month))
str(convert) # Month 변수의 Factor값 확인
# $ Month  : Factor w/ 5 levels "5","6","7","8"

convert # Ozone Solar.R Wind Temp Month Day
xyplot(Ozone ~ Wind | Month, data=convert, layout=c(5,1))
# 컬럼 제목 : Month 값으로 출력


# [실습] quakes 데이터 셋으로 산점도 그래프 그리기 
head(quakes)
str(quakes) # 'data.frame':  1000 obs. of  5 variables:
range(quakes$stations)

# 지진발생 위치(위도와 경로) 
xyplot(lat~long, data=quakes, pch=".") 
# 그래프를 변수에 저장
tplot <- xyplot(lat~long, data=quakes, pch=".")
# 그래프에 제목 추가
tplot2<-update(tplot,
               main="1964년 이후 태평양에서 발생한 지진위치")
print(tplot2)


# [실습] 산점도 그래프 그리기 
# 1. depth 이산형 변수 범위 확인 
range(quakes$depth)# depth 범위

# 2. depth 변수 리코딩 : 6개의 범주(100단위)로 코딩 변경
quakes$depth2[quakes$depth >=40 & quakes$depth <=150] <- 1
quakes$depth2[quakes$depth >=151 & quakes$depth <=250] <- 2
quakes$depth2[quakes$depth >=251 & quakes$depth <=350] <- 3
quakes$depth2[quakes$depth >=351 & quakes$depth <=450] <- 4
quakes$depth2[quakes$depth >=451 & quakes$depth <=550] <- 5
quakes$depth2[quakes$depth >=551 & quakes$depth <=680] <- 6

# 3. 리코딩 변수(depth2)를 조건으로 산점도 그래프 그리기
convert <- transform(quakes, depth2=factor(depth2))
xyplot(lat~long | depth2, data=convert)


# [실습] 동일한 패널에 2개의 y축에 값을 표현
xyplot(Ozone + Solar.R ~ Wind | factor(Month), data=airquality,
       col=c("blue","red"),layout=c(5,1))


# 2.6 데이터 범주화 

# [실습] equal.count() 함수 이용 이산형 변수 범주화 

# (1) 1~150을 대상으로 겹치지 않게 4개 영역으로 범주화
numgroup<- equal.count(1:150, number=4, overlap=0)
numgroup

# (2) 지진의 깊이를 5개 영역으로 범주화
depthgroup<-equal.count(quakes$depth, number=5, overlap=0)
depthgroup

# [실습] 범주화된 변수(depthgroup)를 조건으로 산점도 그래프 그리기 
xyplot(lat ~ long | depthgroup, data=quakes,
       main="Fiji Earthquakes(depthgruop)",
       ylab="latitude", xlab="longitude", pch="@",col='red' )

# [실습] 수심과 리히터규모 변수를 동시에 적용하여 산점도 그래프 그리기 
magnitudegroup<-equal.count(quakes$mag, number=2, overlap=0)
magnitudegroup

# magnitudegroup변수 기준으로 플로팅
xyplot(lat ~ long | magnitudegroup, data=quakes,
       main="Fiji Earthquakes(magjitude)",
       ylab="latitude", xlab="longitude", pch="@", col='blue')


# 수심과 리히터 규모를 동시에 표현(2행 5열 패널 구조)
xyplot(lat ~ long | depthgroup*magnitudegroup, data=quakes,
       main="Fiji Earthquakes",
       ylab="latitude", xlab="longitude",
       pch="@",col=c("red","blue"))


# [실습] 이산형 변수로 리코딩한 뒤에 factor 형으로 변환하여 산점도 그래프 그리기 
quakes$depth3[quakes$depth >= 39.5 & quakes$depth <= 80.5] <- 'd1' 
quakes$depth3[quakes$depth >= 79.5 & quakes$depth <= 186.5] <- 'd2' 
quakes$depth3[quakes$depth >= 185.5 & quakes$depth <= 397.5] <- 'd3' 
quakes$depth3[quakes$depth >= 396.5 & quakes$depth <= 562.5] <- 'd4' 
quakes$depth3[quakes$depth >= 562.5 & quakes$depth <= 680.5] <- 'd5'

quakes$mag3[quakes$mag >= 3.95 & quakes$mag <= 4.65] <- 'm1' 
quakes$mag3[quakes$mag >= 4.55 & quakes$mag <= 6.45] <- 'm2'

convert <- transform(quakes, depth3=factor(depth3), mag3=factor(mag3))

xyplot(lat ~ long | depth3*mag3, data=convert, 
                    main="Fiji Earthquakes", ylab="latitude", 
                    xlab="longitude", pch="@", col=c("red", "blue"))


# 2.7 조건 그래프 
coplot(lat~long | depth, data=quakes) # 2행3열, 0.5, 사이간격 6
coplot(lat~long | depth, data=quakes, overlap=0.1) # 겹치는 구간 : 0.1
coplot(lat~long | depth, data=quakes, number=5, row=1) # 사이간격 5, 1행 5열

# [실습] 패널과 조건 막대에 색 적용 후 조건 그래프 그리기 
coplot(lat~long | depth, data=quakes, number=5, row=1, panel=panel.smooth)
coplot(lat~long | depth, data=quakes, number=5, row=1, 
       col='blue',bar.bg=c(num='green')) # 패널과 조건 막대 색 


# 2.8 3차원 산점도 그래프 

# [실습] 위도, 경도, 깊이를 이용하여 3차원 산점도 그래프 그리기 
cloud(depth ~ lat * long , data=quakes,
      zlim=rev(range(quakes$depth)), 
      xlab="경도", ylab="위도", zlab="깊이")

# [실습] 테두리와 회전 속성을 추가하여 3차원 산점도 그래프 그리기 
cloud(depth ~ lat * long , data=quakes,
      zlim=rev(range(quakes$depth)), 
      panel.aspect=0.9,
      screen=list(z=45,x=-25),
      xlab="경도", ylab="위도", zlab="깊이")


## 3. 기하학적 기법 시각화

# 3.1 qplot() 함수 

install.packages("ggplot2") # 패키지 설치
library(ggplot2)
data(mpg) # 데이터 셋 가져오기
str(mpg) # map 데이터 셋 구조 보기
head(mpg) # map 데이터 셋 내용 보기 
summary(mpg) # 요약 통계량
table(mpg$drv) # 구동방식 빈도수 


# (1) 한 개 변수 대상 qplot() 함수 적용  
qplot(hwy, data=mpg) # 세로막대 그래프
#  fill 속성 : hwy 변수를 대상으로 drv변수에 색 채우기(누적 막대그래프) 
qplot(hwy, data=mpg, fill=drv) # fill 옵션 적용
# binwidth 속성 : 막대 폭 지정 옵션
qplot(hwy, data=mpg, fill=drv, binwidth=2) # binwidth 옵션 적용 
# facets 속성 : drv변수 값으로 칼럼단위와 행 단위로 패널 생성
qplot(hwy, data=mpg, fill=drv, facets=.~ drv, binwidth=2) # 열 단위 패널 생성
qplot(hwy, data=mpg, fill=drv, facets=drv~., binwidth=2) # 행 단위 패널 생성


# (2) 두 개 변수 대상 qplot() 함수 적용 
qplot(displ, hwy, data=mpg)# mpg 데이터셋의 displ과 hwy변수 이용
# displ, hwy 변수 대상으로 drv변수값으로 색상 적용 산점도 그래프
qplot(displ, hwy, data=mpg, color=drv)

# [실습]  displ과 hwy 변수와의 관계를 drv로 구분
qplot(displ, hwy, data=mpg, color=drv, facets=.~ drv)
# mpg 데이터셋의 displ과 hwy변수 이용

# (3) 미적 요소 맵핑(mapping) 
head(mtcars)
qplot(wt, mpg, data=mtcars, color=factor(carb)) # 색상 적용
qplot(wt, mpg, data=mtcars, size=qsec, color=factor(carb)) # 크기 적용
qplot(wt, mpg, data=mtcars, size=qsec, color=factor(carb), shape=factor(cyl))#모양 적용 
mtcars$qsec


# (4) 기하학적 객체 적용  
head(diamonds) 
# geom="bar" -> clarity변수 대상 cut변수로 색 채우기
qplot(clarity, data=diamonds, fill=cut, geom="bar") # 레이아웃에 색 채우기
qplot(clarity, data=diamonds, colour=cut, geom="bar") # 테두리 색 적용


# geom="point"
qplot(wt, mpg, data=mtcars, size=qsec, geom="point")
# cyl 변수의 요인으로 point 크기 적용, carb 변수의 요인으로 포인트 색 적용
qplot(wt, mpg, data=mtcars, size=factor(cyl), color=factor(carb), geom="point")
# qsec변수로 포인트 크기 적용, cyl 변수의 요인으로 point 모양 적용
qplot(wt, mpg, data=mtcars, size=qsec, color=factor(carb), 
      shape=factor(cyl), geom="point")

# geom="smooth"
qplot(wt, mpg, data=mtcars, geom=c("point", "smooth"))
qplot(wt, mpg, data=mtcars, color=factor(cyl), geom=c("point", "smooth"))
# cyl변수 요인으로 색상 적용


# geom="line"
qplot(mpg, wt, data=mtcars, color=factor(cyl), geom="line")
qplot(mpg, wt, data=mtcars, color=factor(cyl), geom=c("point", 'line'))


# 3.2 ggplot() 함수

# (1) 미적 요소 맵핑 
p <- ggplot(diamonds, aes(carat, price, color=cut))
p+geom_point() 

# (2) 기하학적 객체 적용 
p<- ggplot(mtcars, aes(mpg,wt,color=factor(cyl)))
p+geom_line() # line 추가

# geom_point()함수  레이어 추가
p<- ggplot(mtcars, aes(mpg,wt,color=factor(cyl)))
p+geom_point()  # point 추가

# (3) 미적 요소 맵핑과 기하학적 객체 적용  
p <- ggplot(diamonds, aes(price)) 
p + stat_bin(aes(fill=cut), geom="bar") 
p + stat_bin(aes(fill=..density..), geom="bar") 
  
p <- ggplot(diamonds, aes(price)) 
p + stat_bin(aes(fill=cut), geom="area") 
p + stat_bin(aes(color=cut, size=..density..), geom="point") 

# (4) 테마(Thema) 적용 
p <- ggplot(diamonds, aes(carat, price, color=cut)) 
p <- p + geom_point() + ggtitle("다이아몬드 무게와 가격의 상관관계") 
print(p) 

p + theme( 
      title=element_text(color="blue", size=25),
      axis.title=element_text(size=14, face="bold"),   
      axis.title.x=element_text(color="green"),
      axis.title.y=element_text(color="green"), 
      axis.text=element_text(size=14),   
      axis.text.y=element_text(color="red"), 
      axis.text.x=element_text(color="purple"), 
      legend.title=element_text(size=20, face="bold",color="red"), 
      legend.position="bottom",
      legend.direction="horizontal" )
           
           
# 3.3 ggsave()함수  

p <- ggplot(diamonds, aes(carat, price, color=cut))
p + geom_point()  # point 추가
ggsave(file="C:/Rwork/output/diamond_price.pdf") # 가장 최근 그래프 저장
ggsave(file="C:/Rwork/output/diamond_price.jpg", dpi=72)

# 변수에 저장된 그래프 저장 
p <- ggplot(diamonds, aes(clarity))
p <- p+geom_bar(aes(fill=cut), position="fill")  # bar 추가
ggsave(file="C:/Rwork/output/bar.png", plot=p, width=10, height=5)



## 4. 지도 공간 기법 시각화
     
# 4.1 Google Static Maps API 이용 

# [실습] 지도 관련 패키지 설치
library(ggplot2)          # ggplot2 패키지 로딩
install.packages("ggmap") # ggmap 패키지 설치
library(ggmap)           # ggmap 패키지 로딩
 
# 지도위치정보 가져오기
gc <- geocode("seoul")
center <- as.numeric(gc)
center # 위도,경도

# [실습] 지도 정보 생성하기
map <- get_googlemap(center = center, language="ko-KR", color = "bw", scale = 2 )

# [실습] 지도 이미지 그리기
ggmap(map, extent = 'device')

# [실습] 지도 위에 marker 삽입하기 
df <- round(data.frame(x=jitter(rep(-95.36, 25), amount=.3), 
              y=jitter(rep(29.76, 25), amount=.3) ), digits=2)

map <- get_googlemap('houston', markers=df, path=df, scale=2)

ggmap(map, extent = 'device')


# 4.2 종합지도 서비스 관련 API 이용  

# [실습] roadmap 타입으로 지도 그리기
map <- get_map(location ="london", zoom=14, maptype='roadmap', scale=2)
# get_map("중심지역", 확대비율, 지도유형) : ggmap에서 제공하는 함수 
ggmap(map, size=c(600,600), extent='device')

# [실습] watercolor 타입으로 지도 그리기
map <- get_map(location ="seoul", zoom=8, maptype='watercolor', scale=2)
ggmap(map, size=c(600,600), extent='device')


# 4.3 지도 이미지에 레이어 적용  

# [실습] 서울지역 4년제 대학교 위치 표시 
university <- read.csv("C:/Rwork/Part-II/university.csv",header=T)
university # # 학교명","LAT","LON"

# 레이어1 : 정적 지도 생성 
kor <- get_map('seoul', zoom = 11, maptype = 'watercolor')
ggmap(kor)

# 레이어2 : 지도위에 포인트 추가 
ggmap(kor)+geom_point(data=university, aes(x=LON, y=LAT,color=factor(학교명)),size=3)
kor.map <- ggmap(kor)+geom_point(data=university, aes(x=LON, y=LAT,color=factor(학교명)),size=3)

# 레이어3 : 지도위에 텍스트 추가
kor.map + geom_text(data=university, aes(x=LON+0.01, y=LAT+0.01,label=학교명),size=5)


# [실습] 지도 저장하기
ggsave("C:/Rwork/output/university1.png",width=10.24,height=7.68)
# 밀도 적용 파일 저장
ggsave("C:/Rwork/output/university2.png",dpi=1000) # 9.21 x 7.68 in image


#  4.4 공간 지도 시각화 실습  

# 2015년도 06월 기준 대한민국 인구수
pop <- read.csv("C:/Rwork/Part-II/population201506.csv",header=T,
                stringsAsFactors = F)

library(stringr)
region <- pop$지역명   
lon <- pop$LON # 경도
lat <- pop$LAT # 위도
# 세대수 숫자 변환
house <- as.numeric(str_replace_all(pop$세대수, ',',''))  

# 위도,경도,세대수 이용 데이터프레임 생성
df <- data.frame(region, lon,lat,house)

# [실습] 다양한 지도 유형
# maptype='terrain'
map1 <- get_map("daegu", zoom=7 ,  maptype='terrain')
map2 <- ggmap(map1)
map3 <- map2 + geom_point(aes(x=lon,y=lat,colour=house,size=house),data=df)
map3 + geom_text(data=df, aes(x=lon+0.01, y=lat+0.18,label=region),size=3)

# maptype='satellite'
map1 <- get_map("daegu", zoom=7 ,  maptype='satellite')
map2 <- ggmap(map1)
map3 <- map2 + geom_point(aes(x=lon,y=lat,colour=house,size=house),data=df)
map3 + geom_text(data=df, aes(x=lon+0.01, y=lat+0.18,label=region),size=3)

# maptype='roadmap'
map1 <- get_map("daegu", zoom=7 ,  maptype='roadmap')
map2 <- ggmap(map1)
map3 <- map2 + geom_point(aes(x=lon,y=lat,colour=house,size=house),data=df)
map3 + geom_text(data=df, aes(x=lon+0.01, y=lat+0.18,label=region),size=3)

# maptype='hybrid'
map1 <- get_map("jeonju", zoom=7,  maptype='hybrid')
map2 <- ggmap(map1)
map3 <- map2 + geom_point(aes(x=lon,y=lat,colour=house,size=house),data=df)
map3 + geom_text(data=df, aes(x=lon+0.01, y=lat+0.18,label=region),size=3)
map3 + geom_density2d()
