# ui.R

library(shiny)

shinyUI(fluidPage(
 
  titlePanel("머리글 관련 함수"),
  
    sidebarLayout(
    sidebarPanel(h2("Header title")),
    
    mainPanel(  # 머리글 관련 함수 사용 예 
      h6("Sixth level header title", align = "center"),
      h5("Fifth level header title", align = "center"),
      h4("Fourth level header title", align = "center"),
      h3("Third level header title", align = "center"),
      h2("Second level header title", align = "center"),
      h1("First level header title")
    )
  )
))
