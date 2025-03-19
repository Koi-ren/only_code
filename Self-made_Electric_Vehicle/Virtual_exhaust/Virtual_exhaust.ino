#define TRIG 6     // TRIG 핀 설정 (초음파 보내는 핀)
#define ECHO 7     // ECHO 핀 설정 (초음파 받는 핀)
#define relayPin1 11 // GPIO pin connected to the SSR
#define relayPin2 12 // GPIO pin connected to the SSR


unsigned long timeCurr;  // 현재 시간을 저장하는 변수
unsigned long timePrev = 0; // 이전 시간을 저장하는 변수
const unsigned long interval = 200; // 거리 측정 간격 (밀리초 단위)
long duration;  // 초음파가 되돌아오는 데 걸리는 시간
int distance;   // 계산된 거리

void superSonic_uses() {
  timeCurr = millis();  // 현재 시간을 밀리초 단위로 가져옴

  if (timeCurr - timePrev >= interval) {  // interval 밀리초마다 초음파 측정
    timePrev = timeCurr;  // timePrev 갱신

    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);

    duration = pulseIn(ECHO, HIGH); // 초음파가 되돌아오는 시간 측정
    distance = duration * 0.034 / 2; // 거리 계산 (음속: 340m/s -> 0.034 cm/us)

    Serial.print("Measured distance: ");
    Serial.println(distance);

    // 거리 조건에 따라 SSR 제어
    if (distance <= 10) {
      digitalWrite(relayPin1, HIGH); // SSR 활성화
      digitalWrite(relayPin2, HIGH); // SSR 활성화
    } else {
      digitalWrite(relayPin1, LOW); // SSR 비활성화
      digitalWrite(relayPin2, LOW); // SSR 활성화
    }
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(relayPin1, OUTPUT);
  pinMode(relayPin2, OUTPUT);
}

void loop() {
  superSonic_uses();  // 주기적으로 거리 측정을 수행
}
