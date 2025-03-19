# ui.R

library(shiny)

shinyUI(fluidPage ( # pageWithSidebar
  
  #헤더 패널 - 애플리케이션 제목
  #headerPanel("제목 패널-title panel"),
  
  # Application title
  titlePanel("제목 패널-title panel"),
  
  # 측면 패널
  sidebarPanel("측면 패널 - sidebar panel"), 
  
  # 메인 패널
  # mainPanel("메인 패널 - main panel")
  mainPanel(
    h3("iris 요약통계량 결과"),
    
    verbatimTextOutput("summary") 
    #textOutput("summary")
  )
))
