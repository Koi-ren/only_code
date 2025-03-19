# ui.R

library(shiny)

shinyUI(fluidPage ( 
  
  # 애플리케이션 제목
  # Application title
  titlePanel("제목 패널-title panel"),
  
  # 측면 패널
  sidebarPanel("측면 패널 - sidebar panel"), 
  
  # 메인 패널
  mainPanel("메인 패널 - main panel")
  
))
