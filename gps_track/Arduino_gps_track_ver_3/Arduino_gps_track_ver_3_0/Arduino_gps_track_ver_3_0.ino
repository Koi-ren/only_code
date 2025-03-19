#include <Wire.h> // I2C 연결에 필요
#include <SoftwareSerial.h>
#include <TinyGPSPlus.h> // TinyGPSPlus 라이브러리 사용
#include <SparkFun_u-blox_GNSS_Arduino_Library.h>

float lat_1, lon_1, lat_2, lon_2, lat_3, lon_3;
long alt;
byte siv;

long lastTime = 0;

SoftwareSerial gpsSerial_1(4, 3);
SoftwareSerial gpsSerial_2(7, 6);  // 세미콜론 추가

TinyGPSPlus gps;  // TinyGPSPlus 사용
SFE_UBLOX_GNSS myGNSS;  // NEO M9N 사용

void setup() {
  Serial.begin(9600);
  while (!Serial); // 터미널을 열 때까지 대기
  Serial.println("Get your Position!");

  Wire.begin();

  // myGNSS.enableDebugging(); // 주석 해제시 디버그 메시지 활성화

  if (myGNSS.begin() == false) { // Wire 포트를 사용하여 u-blox 모듈에 연결
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }

  myGNSS.setI2COutput(COM_TYPE_UBX); // I2C 포트를 UBX만 출력하도록 설정 (turn off NMEA noise)
  myGNSS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); // 통신 포트 설정만 플래시와 BBR에 저장

  Serial.println("Start GPS... ");
  gpsSerial_1.begin(9600);
  gpsSerial_2.begin(9600);
}

void loop() {
  if (millis() - lastTime > 1000) {
    lastTime = millis(); // 타이머 업데이트

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

    // NEO M9N 데이터 처리
    lat_3 = myGNSS.getLatitude();
    lon_3 = myGNSS.getLongitude();
    alt = myGNSS.getAltitude();
    siv = myGNSS.getSIV();

    // 시리얼 모니터로 GPS 데이터 출력
    Serial.println("GPS Data:");
    Serial.print("GPS 1: Latitude = "); Serial.print(lat_1, 6); 
    Serial.print(", Longitude = "); Serial.println(lon_1, 6);

    Serial.print("GPS 2: Latitude = "); Serial.print(lat_2, 6); 
    Serial.print(", Longitude = "); Serial.println(lon_2, 6);

    Serial.print("GPS 3 (NEO M9N): Latitude = "); Serial.print(lat_3, 6); 
    Serial.print(", Longitude = "); Serial.print(lon_3, 6); 
    Serial.print(", Altitude = "); Serial.print(alt); 
    Serial.print(" meters, SIV = "); Serial.println(siv);

    Serial.println();
  }
}