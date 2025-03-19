#include <Wire.h>
#include <SoftwareSerial.h>
#include <TinyGPSPlus.h> // TinyGPSPlus 라이브러리 사용

float lat_1, lon_1;

SoftwareSerial gpsSerial_1(4, 3); // 첫 번째 TinyGPS 모듈 (TX, RX)
TinyGPSPlus gps;  // TinyGPSPlus GPS 모듈 사용

void setup() {
  Serial.begin(9600);
  while (!Serial); // 터미널을 열 때까지 대기
  Serial.println("Get your Position from Board B via Serial!");

  Wire.begin(8);  // I2C 슬레이브 주소 8번으로 설정
  Wire.onRequest(requestEvent); // I2C 마스터 요청 처리 함수 등록

  gpsSerial_1.begin(9600);  // 시리얼 통신 시작

  Serial.println("Start GPS via Serial... ");
}

void loop() {
  // GPS 데이터 읽기
  while (gpsSerial_1.available()) { 
    if (gps.encode(gpsSerial_1.read())) {
      lat_1 = gps.location.lat();
      lon_1 = gps.location.lng();
    }
  }
  
  delay(1000); // 1초 간격으로 데이터 업데이트
}

// I2C 마스터의 요청이 있을 때 GPS 데이터를 전송
void requestEvent() {
  Wire.write((byte*)&lat_1, sizeof(lat_1));
  Wire.write((byte*)&lon_1, sizeof(lon_1));
}
