#include <Wire.h> // I2C 통신을 위해 필요
#include <SparkFun_u-blox_GNSS_Arduino_Library.h> // SparkFun u-blox GNSS 라이브러리

float lat_3, lon_3;
long alt;
byte siv;

// NEO M9N GPS 모듈 사용
SFE_UBLOX_GNSS myGNSS;

void setup() {
  Serial.begin(9600);
  while (!Serial); // 터미널을 열 때까지 대기
  Serial.println("Get your Position from Board A via I2C!");

  Wire.begin();  // I2C 마스터 모드로 시작
  // myGNSS.enableDebugging(); // 주석 해제 시 디버그 메시지 활성화

  if (myGNSS.begin() == false) { // Wire 포트를 사용하여 u-blox 모듈에 연결
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1); // 모듈이 감지되지 않으면 멈춤
  }

  myGNSS.setI2COutput(COM_TYPE_UBX); // I2C 포트를 UBX만 출력하도록 설정 (NMEA 노이즈 제거)
  myGNSS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); // 통신 포트 설정만 플래시와 BBR에 저장

  Serial.println("Start GPS via I2C... ");
}

void loop() {
  delay(1000); // 1초 간격으로 데이터 읽기

  // NEO M9N 데이터 처리
  lat_3 = myGNSS.getLatitude();
  lon_3 = myGNSS.getLongitude();
  alt = myGNSS.getAltitude();
  siv = myGNSS.getSIV();

  // 시리얼 모니터로 NEO M9N GPS 데이터 출력
  Serial.println("GPS Data from NEO M9N (Board A):");
  Serial.print("Latitude = "); Serial.print(lat_3, 6);
  Serial.print(", Longitude = "); Serial.print(lon_3, 6);
  Serial.print(", Altitude = "); Serial.print(alt);
  Serial.print(" meters, SIV = "); Serial.println(siv);

  // I2C를 통해 보드 B에서 GPS 데이터를 수신
  Wire.requestFrom(8, 8);  // 슬레이브 주소 8번에서 8바이트 읽기
  
  // 보드 B로부터 수신한 데이터 처리
  float lat_1 = 0, lon_1 = 0;
  if (Wire.available() >= 8) {
    Wire.readBytes((char*)&lat_1, sizeof(lat_1));
    Wire.readBytes((char*)&lon_1, sizeof(lon_1));
    
    // 보드 B로부터 받은 GPS 데이터를 시리얼 모니터에 출력
    Serial.println("GPS Data from Board B:");
    Serial.print("Latitude = "); Serial.print(lat_1, 6);
    Serial.print(", Longitude = "); Serial.println(lon_1, 6);
  }
  Serial.println();
}
