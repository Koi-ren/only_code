
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)

shinyServer(function(input, output) {

  output$distPlot <- renderPlot({

    # generate bins based on input$bins from ui.R
    x    <- faithful[, 2] # 간헐천의 대기 칼럼으로 x 값 할당 
    bins <- seq(min(x), max(x), length.out = input$bins+1)

    # draw the histogram with the specified number of bins
    hist(x, breaks = bins, col = 'darkgray', border = 'white')

  })

})

#########################################
faithful # Old Faithful Geyser Data
# 올드페이스풀 간헐천  : 미국 옐로스톤 국립공원에 있는 간헐천
# 272개의 관측치와 2개의 칼럼으로 구성 eruptions(폭발,분화), waiting(대기)
# 간헐천의 폭발과 대기에 관한 2개이 칼럼으로 구성됨 
data()
x <- faithful[,2] # 간헐천의 대기 값 - seq()의 시작과 종료
bins <-3 # input 값은 seq의 길이(예: 2이면 3)  
# 형식1) seq(from, to, by, length.out)
# 형식2) seq(from, to, length.out)
bins <- seq(min(x), max(x), length.out = bins + 1)
bins
hist(x, breaks = bins) # breaks = bins : 히스토그램의 셀 수 
#########################################
# <정리> 
# 스크롤바를 이용하여 선택한 값에 따라서 히스토그램의 셀 수가 결정된다.
# 히스토그램에서 그려지는 계급과 빈도수는 간헐천의 두번째 칼럼값이 
# 그려지는데, 이때 seq()함수는 간헐천(x)의 최솟값 부터 최대값까지 
# 스크롤바에 의해서 선택한 값에 1를 더한 값 만큼 히스토그램의 셀 수를
# 그려준다.


