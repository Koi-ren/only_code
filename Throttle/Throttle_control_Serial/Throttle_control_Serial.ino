#define Throttle A0
int Throttle_value = 0;
int con_Throttle_value;

void setup() {
  
  Serial.begin(9600);
  pinMode(Throttle, OUTPUT);
  analogWrite(Throttle, Throttle_value);
}

void loop() {
  
  if(Serial.available()){
    con_Throttle_value = Serial.read();
    Throttle_value = map(con_Throttle_value, 0, 100, 853, 300);
    analogWrite(Throttle, Throttle_value);
    delay(5000);
  }

}
