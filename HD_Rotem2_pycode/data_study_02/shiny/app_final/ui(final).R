# shiny project 생성
# 1. New Project 
# 2. Project 디렉터리와 폴더 생성
# 3. 폴더에 ui.R과 server.R 생성됨 
# 4. Project 실행 -> Run App 실행 -> 브라우저에서 앱 결과 확인 
# 5. R session 차단 됨, 해제 : server 종료 : ESC


# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)

shinyUI(fluidPage(

  # Application title
  titlePanel("Old Faithful Geyser Data"),

  # Sidebar with a slider input for number of bins
  sidebarLayout(
    sidebarPanel(
      sliderInput("bins","Start button click!!",
                  min = 10,
                  max = 50,
                  value = 10, step=5,
                  animate = animationOptions(interval = 1000, 
                                             loop = T, 
                                             playButton = 'Start'))
    ),

    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("distPlot")
    )
  )
))
