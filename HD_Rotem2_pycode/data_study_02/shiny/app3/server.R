# server.R

library(shiny)

shinyServer(function(input, output) {
  
  # ui.R에서 파라미터를 넘겨주면 reactive함수에 의해서 리액션이 수행된다.
  # Parameter와 Value 칼럼으로 데이터프레임을 생성하는 sliderValues()함수 생성
  sliderValues <- reactive({
    
    # data frame 생성(Parameter과 value 칼럼) 
    data.frame(
      Parameter = "Integer",
      Value = as.character(input$integer))
  }) 
  
  # HTML table 양식으로 값을 넘겨준다.
  output$values <- renderTable({ # 함수 호출 결과값을 values에 저장하여 넘김
    sliderValues() # sliderValues함수 호출 
  })
})
