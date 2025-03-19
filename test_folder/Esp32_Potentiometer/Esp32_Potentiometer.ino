void setup() {
  Serial.begin(115200); // 시리얼 통신 속도 설정
  analogReadResolution(12); // 아날로그 입력 해상도 설정 (0~4095)
}

void loop() {
  // GPIO 34와 35에서 값을 읽기
  int analogValue1 = analogRead(3); // 핀 34에서 아날로그 값 읽기
  int analogValue2 = analogRead(1); // 핀 35에서 아날로그 값 읽기

  // 밀리볼트(mV) 단위로 변환
  int analogVolts1 = analogReadMilliVolts(3);
  int analogVolts2 = analogReadMilliVolts(1);

  // 시리얼 모니터에 출력
  Serial.printf("ADC value 1 (pin 34) = %d, Volts = %d mV\n", analogValue1, analogVolts1);
  Serial.printf("ADC value 2 (pin 35) = %d, Volts = %d mV\n", analogValue2, analogVolts2);

  delay(100); // 일정 시간 지연
}
