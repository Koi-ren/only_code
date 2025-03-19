#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  mpu.initialize();
  if (mpu.testConnection()) {
    Serial.println("MPU6050 연결 성공");
  } else {
    Serial.println("MPU6050 연결 실패");
  }
}

void loop() {
  int16_t ax, ay, az;
  int16_t gx, gy, gz;

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // 시리얼 포트를 통해 데이터를 출력
  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.print(az); Serial.print(",");
  Serial.print(gx); Serial.print(",");
  Serial.print(gy); Serial.print(",");
  Serial.println(gz);

  delay(100);  // 100ms 지연
}
