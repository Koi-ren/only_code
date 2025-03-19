//초음파 선언부
#define TRIG_R 9 //TRIG_1 핀 설정 (초음파 보내는 핀)
#define ECHO_R 8 //ECHO_1 핀 설정 (초음파 받는 핀) 
#define TRIG_L 7 //TRIG_2번 핀 (초음파 보내는 핀)
#define ECHO_L 6 //ECHO_2 핀 설정 (초음파 받는 핀) 

long duration_R, distance_R, duration_L, distance_L;

//LED 선언부
#define LED_R 2 //오른쪽 물체 감지 시 깜빡이는 LED
#define LED_L 1 //왼쪽 물체 감지 시 깜빡이는 LED

void setup() {
  Serial.begin(9600); 
  //초음파
  pinMode(TRIG_R, OUTPUT);
  pinMode(ECHO_R, INPUT);
  pinMode(TRIG_L, OUTPUT);
  pinMode(ECHO_L,  INPUT);
  //LED
  pinMode(LED_R, OUTPUT);
  pinMode(LED_L, OUTPUT)
}

void loop() {

  //초음파 활용부 시작
  digitalWrite(TRIG_R, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_R, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_R, LOW);

  duration_R = pulseIn (ECHO_R, HIGH);
  distance_R = duration_R * 17 / 1000;

  digitalWrite(TRIG_L, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_L, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_L, LOW);

  duration_L = pulseIn (ECHO_R, HIGH);
  distance_L = duration_L * 17 / 1000;
  //초음파 활용부 끝

  //LED 활용부 시작
  if(distance_R < 30) {
    digitalWrite(LED_R, HIGH);
  }
  else {
    digitalWrite(LED_R, LOW);
  }

  if(distance_L < 30) {
    digitalWrite(LED_L, HIGH);
  }
  else {
    digitalWrite(LED_L, LOW);
  }
  //LED활용부 끝
  delay(100)
}
