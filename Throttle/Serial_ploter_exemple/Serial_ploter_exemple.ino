int a = 0;
int b = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print(a);
  Serial.print(',');
  Serial.println(b);

  if(a>150){
    a = a-5;
  }
  else{
    a = a+5;
  }
  if(b>100){
    b = b-3;
  }
  else{
    b = b+3;
  }
  delay(200);
}
