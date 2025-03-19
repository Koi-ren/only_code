//실제 스로틀 입력 값 측정 - 아날로그 값으로 1초 간격 측정

#define Throttle A0  //스로틀 연결핀 A0
#define interval 1000  //1초로 제한, 본 값으로 유동 가능
float Throttle_value = 0;  //아날로그 값으로 읽을 스로틀 값을 실수형으로 선언
float filtered_value;  //low-pass filter를 통해 필터링된 값
float sensitivity = 0.1;  //90% 값을 저장하고 10%를 현재값으로 사용하겠다는 뜻
unsigned long timeCurr = 0;  // 현재시간 값

void Throttle_Read()  //interval 밀리초에 한번 스로틀 값을 읽고 필터링된 값을 내보내는 함수
{
  timeCurr = millis();
  if(timeCurr%interval == 0)
  {
    Throttle_value = analogRead(Throttle);
    filtered_value = filtered_value*(1 - sensitivity) + Throttle_value*sensitivity;  //low-pass filter
    
    Serial.print(F(" Throttle_value: "));
    Serial.print(Throttle_value);  //입력된 신호값
    
    Serial.print(F(" filtered_value: "));  
    Serial.print(filtered_value);  //필터링된 신호값
    
    Serial.println();
  }
}

void setup()
{
    Serial.begin(9600);
    pinMode(Throttle, INPUT);
    Throttle_value = analogRead(Throttle);
    filtered_value = Throttle_value;
    Serial.println("Read Throttle value");
    delay(300);
    Serial.println("with low pass filter");
    delay(500);
}

void loop()
{
  Throttle_Read();
}