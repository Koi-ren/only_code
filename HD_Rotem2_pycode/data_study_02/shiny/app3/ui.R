# ui.R

library(shiny)

shinyUI(fluidPage(
 
  titlePanel("Sliders"),
  
    sidebarLayout(
    sidebarPanel(  # 슬라이더 위젯 생성 
      sliderInput("integer", "Integer:",
                  min=0, max=1000, value=500)
      ),
    mainPanel(  # server.R에서 넘긴 값을 받음 
      tableOutput("values") # HTML 테이블 형식으로 출력 
    )
  )
))
