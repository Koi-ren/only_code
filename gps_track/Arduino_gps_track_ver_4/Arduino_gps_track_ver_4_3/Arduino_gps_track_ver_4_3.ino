#include <Wire.h> // I2C 통신을 위해 필요
#include <SparkFun_u-blox_GNSS_Arduino_Library.h> // SparkFun u-blox GNSS 라이브러리
#define LED 7

float lat_1, lon_1, lat_2, lon_2, lat_sum, lon_sum, lat_average, lon_average;
long alt_1, alt_2, alt_sum, alt_average;
byte siv_1, siv_2;

long lastTime = 0;
unsigned int siv_sum = 0;
float siv_average = 0;

SFE_UBLOX_GNSS myGNSS;  // NEO M9N 사용

void setup() {
  Serial.begin(115200);
  while (!Serial); // 터미널을 열 때까지 대기
  Serial.println("Get your Position!");

  Wire.begin();

  pinMode(LED, OUTPUT);

  initializeGNSS(1, "GNSS_1");
  initializeGNSS(3, "GNSS_2");
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

    siv_sum = siv_1 + siv_2;
    siv_average = siv_sum / 2.0;

    lat_sum = lat_1 + lat_2;
    lat_average = lat_sum / 2.0;

    lon_sum = lon_1 + lon_2;
    lon_average = lon_sum / 2.0;

    alt_sum = alt_1 + alt_2;
    alt_average = alt_sum / 2.0;

    if(siv_average >= 9){
      digitalWrite(LED, HIGH);}
    else{
      digitalWrite(LED, LOW);}

    Serial.print(F("Lat: "));
    Serial.print(lat_average);
    Serial.print(F(" Long: "));
    Serial.print(lon_average);
    Serial.print(F(" Alt: "));
    Serial.println(alt_average);
  }
}
