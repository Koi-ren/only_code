# ui.R

library(shiny)

shinyUI(fluidPage(
  titlePanel("이미지 표현 함수 예"),
  sidebarLayout(
    sidebarPanel(h2("image display")),
    mainPanel(
      img(src="r.png", height = 300, width = 600)
    )
  )
))
