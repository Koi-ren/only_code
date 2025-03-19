#include <Wire.h> // I2C 통신을 위해 필요
#include <SparkFun_u-blox_GNSS_Arduino_Library.h> // SparkFun u-blox GNSS 라이브러리

float lat_1, lon_1, lat_2, lon_2, lat_3, lon_3;
long alt_1, alt_2, alt_3;
byte siv_1, siv_2, siv_3;

long lastTime = 0;
unsigned int sum = 0;
float average_siv = 0;

SFE_UBLOX_GNSS myGNSS;  // NEO M9N 사용

void setup() {
  Serial.begin(9600);
  while (!Serial); // 터미널을 열 때까지 대기
  Serial.println("Get your Position!");

  Wire.begin();

  initializeGNSS(1, "GNSS_1");
  initializeGNSS(3, "GNSS_2");
  //initializeGNSS(7, "GNSS_3");
}

void TCA9548A(uint8_t bus) {
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}

void initializeGNSS(uint8_t bus, const char* label) {
  TCA9548A(bus);
  // myGNSS.enableDebugging(); // 주석 해제시 디버그 메시지 활성화
  if (myGNSS.begin() == false) { // Wire 포트를 사용하여 u-blox 모듈에 연결
    Serial.print(F("u-blox "));
    Serial.print(label);
    Serial.println(F(" not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }

  myGNSS.setI2COutput(COM_TYPE_UBX); // I2C 포트를 UBX만 출력하도록 설정 (turn off NMEA noise)
  myGNSS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); // 통신 포트 설정만 플래시와 BBR에 저장

  Serial.print("Start ");
  Serial.println(label);
}

void loop() {
  if (millis() - lastTime > 1000) {
    lastTime = millis(); // 타이머 업데이트

    TCA9548A(1);
    lat_1 = myGNSS.getLatitude();
    lon_1 = myGNSS.getLongitude();
    alt_1 = myGNSS.getAltitude();
    siv_1 = myGNSS.getSIV();

    TCA9548A(3);
    lat_2 = myGNSS.getLatitude();
    lon_2 = myGNSS.getLongitude();
    alt_2 = myGNSS.getAltitude();
    siv_2 = myGNSS.getSIV();


    //TCA9548A(7);
    //lat_3 = myGNSS.getLatitude();
    //lon_3 = myGNSS.getLongitude();
    //alt_3 = myGNSS.getAltitude();
    //siv_3 = myGNSS.getSIV();

//    sum = siv_1 + siv_2 + siv_3;
//    average_siv = sum / 3.0;
    sum = siv_1 + siv_2;
    average_siv = sum / 2.0;


    Serial.println(F("GNSS_1:"));
    Serial.print(F("Lat: "));
    Serial.print(lat_1);
    Serial.print(F(" Long: "));
    Serial.print(lon_1);
    Serial.print(F(" Alt: "));
    Serial.println(alt_1);
    Serial.println();

    Serial.println(F("GNSS_2:"));
    Serial.print(F("Lat: "));
    Serial.print(lat_2);
    Serial.print(F(" Long: "));
    Serial.print(lon_2);
    Serial.print(F(" Alt: "));
    Serial.println(alt_2);
    Serial.println();

    //Serial.println(F("GNSS_3:"));
    //Serial.print(F("Lat: "));
    //Serial.print(lat_3);
    //Serial.print(F(" Long: "));
    //Serial.print(lon_3);
    //Serial.print(F(" Alt: "));
    //Serial.println(alt_3);

    Serial.print(F("Average SIV: "));
    Serial.println(average_siv);

    Serial.println("//////////////////////////////////////////////");
  }
}
