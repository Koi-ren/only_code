# server.R

library(shiny)
data(iris) # 데이터 셋 로드 

shinyServer(function(input, output) {
  
  output$summary <- renderPrint({
    dataset <- iris[-5]
    summary(dataset)
  })
  
})

