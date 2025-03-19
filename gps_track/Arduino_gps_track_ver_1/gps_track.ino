#include <Wire.h> //I2C연결에 필요

#include <SparkFun_u-blox_GNSS_Arduino_Library.h>
SFE_UBLOX_GNSS myGNSS;

long lastTime = 0; //I2C 트래픽을 u_blox 모듈로 제한
void setup(){
  Serial.begin(9600);
  while (!Serial); //터미널을 열 때까지 대기
  Serial.println("Get your Position!");

  Wire.begin();

  //myGNSS.enableDebugging(); //주석 해제시 디버그 메시지 활성화

  if (myGNSS.begin() == false) //Wire 포트를 사용하여 u-blox 모듈에 연결
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }

  myGNSS.setI2COutput(COM_TYPE_UBX); //I2C 포트를 UBX만 출력하도록 설정(turn off NMEA noise)
  myGNSS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); //통신 포트 설정만 플래시와 BBR에 저장
}

void loop()
{
  //새 위치가 사용 가능할 때만 응답. 1초마다 모듈. 더 자주 하면 I2C 트래픽만 증가해 프로그램 버벅거림.
  if (millis() - lastTime > 1000)
  {
    lastTime = millis(); //타이머 업데이트
    
    long latitude = myGNSS.getLatitude();
    Serial.print(F("Lat: "));
    Serial.print(latitude);

    long longitude = myGNSS.getLongitude();
    Serial.print(F(" Long: "));
    Serial.print(longitude);

    long altitude = myGNSS.getAltitude();
    Serial.print(F(" Alt: "));
    Serial.print(altitude);

    byte SIV = myGNSS.getSIV();
    Serial.print(F(" SIV: "));
    Serial.print(SIV);

    Serial.println();
  }
}
