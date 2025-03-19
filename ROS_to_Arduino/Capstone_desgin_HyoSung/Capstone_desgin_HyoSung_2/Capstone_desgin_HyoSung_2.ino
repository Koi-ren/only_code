#include <WiFi.h>

//초음파 선언부
#define TRIG_R 9 //TRIG_1 핀 설정 (초음파 보내는 핀)
#define ECHO_R 8 //ECHO_1 핀 설정 (초음파 받는 핀) 
#define TRIG_L 7 //TRIG_2번 핀 (초음파 보내는 핀)
#define ECHO_L 6 //ECHO_2 핀 설정 (초음파 받는 핀) 

long duration_R, distance_R, duration_L, distance_L;

//LED 선언부
#define LED_R 2 //오른쪽 물체 감지 시 깜빡이는 LED
#define LED_L 4 //왼쪽 물체 감지 시 깜빡이는 LED

//부저 선언부
#define buzzer 3 //라이다 접근 시 소리 출력

int Do = 262;
int Mi = 330;
int Sol = 392;
int Do2 = 523;

void setup() {
  Serial.begin(9600); 
  //초음파
  pinMode(TRIG_R, OUTPUT);
  pinMode(ECHO_R, INPUT);
  pinMode(TRIG_L, OUTPUT);
  pinMode(ECHO_L,  INPUT);
  //LED
  pinMode(LED_R, OUTPUT);
  pinMode(LED_L, OUTPUT);
//부저
  pinMode(buzzer, OUTPUT);
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

  duration_L = pulseIn (ECHO_L, HIGH);
  distance_L = duration_L * 17 / 1000;

  Serial.print("distance_R = ");
  Serial.print(distance_R);
  Serial.print("cm\n");
  Serial.print("distance_L = ");
  Serial.print(distance_L);
  Serial.print("cm\n");
  //초음파 활용부 끝

  //LED 활용부 시작
  if(distance_R < 10) {
    analogWrite(LED_R, 255);
  }
  else {
    analogWrite(LED_R, 0);
  }

  if(distance_L < 10) {
    analogWrite(LED_L, 255);
  }
  else {
    analogWrite(LED_L, 0);
  }
  //LED활용부 끝
  if (distance_L >= 20 && distance_L <= 30) {
    tone(buzzer, Do);
    delay(500);
  } else if (distance_L >= 10 && distance_L < 20) {
    tone(buzzer, Mi);
    delay(500);
  } else if (distance_L >= 5 && distance_L < 10) {
    tone(buzzer, Sol);
    delay(500);
  } else if (distance_L < 5) {
    tone(buzzer, Do2);
    delay(500);
  }  else {
    noTone(buzzer);  // 부저 끄기
  }
  if (distance_R >= 20 && distance_R <= 30) {
    tone(buzzer, Do);
    delay(500);
  } else if (distance_R >= 10 && distance_R < 20) {
    tone(buzzer, Mi);
    delay(500);
  } else if (distance_R >= 5 && distance_R < 10) {
    tone(buzzer, Sol);
    delay(500);
  } else if (distance_R < 5) {
    tone(buzzer, Do2);
    delay(500);
  } else {
    noTone(buzzer);  // 부저 끄기
  }
}
