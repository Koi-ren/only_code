//실제 스로틀 입력 값 측정 - 아날로그 값으로 1초 간격 측정

#define Throttle_1 A0  //스로틀값 입력 연결핀 A0
#define Throttle_2 A1  //스로틀값 출력 연결핀 A1
#define interval 1000  //1초로 제한, 본 값으로 유동 가능
int Throttle_value = 0;  //아날로그 값으로 읽을 스로틀 값을 실수형으로 선언
float Throttle_input_value = 0;  //시리얼통신으로 입력할 스로틀 값
//float sensitivity = 0.1;  //90% 값을 저장하고 10%를 현재값으로 사용하겠다는 뜻
unsigned long timeCurr = 0;  // 현재시간 값
int con_Throttle_value;  //0~100사이 값으로 직관성있게 바꾸는 값

void Throttle_Read()  //interval 밀리초에 한번 스로틀 값을 읽는 함수
{
  timeCurr = millis();
  if(timeCurr%interval == 0)
  {
    Throttle_value = analogRead(Throttle_1);
    
    Serial.print(F(" Throttle_value: "));
    Serial.print(Throttle_value);  //입력된 신호값
    
    Serial.println();
  }
}

void Throttle_control()  //시리얼 통신을 통해 0부터 100까지의 가상 스로틀값을 입력해 모터를 제어하는 함수
{
    if(Serial.available()){
    con_Throttle_value = Serial.read();
    Throttle_input_value = map(con_Throttle_value, 0, 100, 860, 177);
    analogWrite(Throttle_2, Throttle_input_value);
    delay(4000);
    analogWrite(Throttle_2, 860);
    delay(7000);
  }
}

void setup()
{
    Serial.begin(9600);
    pinMode(Throttle_1, INPUT);
    pinMode(Throttle_2, OUTPUT);

    Serial.println("Read Throttle value");
    delay(500);
}

void loop()
{
  Throttle_Read();
  Throttle_control();
}