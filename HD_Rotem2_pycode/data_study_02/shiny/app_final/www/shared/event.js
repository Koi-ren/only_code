// 웹문서가 브라우저에 로딩되면 무명함수 실행 
$(document).ready(function()  {	// script start 
  
  //  start버튼 클릭 시 bins 값을 bins_value 변수에 저장
  $('.play').click(function () {		
	    var bins_value = $("#bins").val();
	    bins_value = Number(bins_value); // 숫자형으로 변경 
	    
	    // 1초 단위로 bins_value값을 텍스트 상자에 표시
      interval = setInterval(function () {
          bins_value = bins_value + 5;
          if(bins_value > 50){
             bins_value = 10;
          }    
	       $('#bins_val').attr("value", bins_value);
      },1000);
  });
	
	// 정지 버튼을 클릭하면 숫자 표시를 정지 
	$('.pause').click(function () {		
     setTimeout(function () {
		    clearInterval(interval);
		 }); 
  });
  
}); // script end  