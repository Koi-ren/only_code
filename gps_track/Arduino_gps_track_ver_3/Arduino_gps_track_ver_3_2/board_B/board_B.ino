#include <SoftwareSerial.h>
#include <TinyGPSPlus.h> // TinyGPSPlus 라이브러리 사용

float lat_1, lon_1, lat_2, lon_2;

SoftwareSerial gpsSerial_1(4, 3); // 첫 번째 TinyGPS 모듈 (TX, RX)
SoftwareSerial gpsSerial_2(7, 6); // 두 번째 TinyGPS 모듈 (TX, RX)

TinyGPSPlus gps;  // TinyGPSPlus GPS 모듈 사용

void setup() {
  Serial.begin(9600);
  while (!Serial); // 터미널을 열 때까지 대기
  Serial.println("Get your Position via Serial!");

  // 시리얼 통신 시작
  gpsSerial_1.begin(9600);
  gpsSerial_2.begin(9600);

  Serial.println("Start GPS via Serial... ");
}

void loop() {
  delay(1000); // 1초 간격으로 데이터 읽기

  // GPS_1 데이터 처리
  while (gpsSerial_1.available()) { 
    if (gps.encode(gpsSerial_1.read())) {
      lat_1 = gps.location.lat();
      lon_1 = gps.location.lng();
    }
  }

  // GPS_2 데이터 처리
  while (gpsSerial_2.available()) {
    if (gps.encode(gpsSerial_2.read())) {
      lat_2 = gps.location.lat();
      lon_2 = gps.location.lng();
    }
  }

  // 시리얼 모니터로 GPS 데이터 출력
  Serial.println("GPS Data from TinyGPS:");
  Serial.print("GPS 1: Latitude = "); Serial.print(lat_1, 6);
  Serial.print(", Longitude = "); Serial.println(lon_1, 6);

  Serial.print("GPS 2: Latitude = "); Serial.print(lat_2, 6);
  Serial.print(", Longitude = "); Serial.println(lon_2, 6);

  Serial.println();
}
