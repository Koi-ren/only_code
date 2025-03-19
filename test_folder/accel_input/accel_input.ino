#define accel A0

void setup() {
  Serial.begin(9600);
  pinMode(A0, OUTPUT);
}

void loop() {
  if(Serial.available()>0)
  {
    int inputValue = Serial.parseInt();

    if(inputValue >= 0 && inputValue <= 1023)
    {
      analogWrite(A0, inputValue);
      Serial.print("엑셀 출력값: ");
      Serial.println(inputValue);
    }
    else
    {
      Serial.print("입력값 유효하지 않음");
    }
  }

}
