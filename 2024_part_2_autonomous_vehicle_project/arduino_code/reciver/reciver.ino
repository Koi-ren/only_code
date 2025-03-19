#include <esp_now.h>
#include <WiFi.h>

#define Led_1 9  // LED 핀 1
#define Led_2 10 // LED 핀 2

typedef struct struct_message {
  int id;
  int speed;
  int angle;
} struct_message;

// 수신한 데이터를 저장할 구조체 정의
struct_message myData;

void onReceive(const esp_now_recv_info *recv_info, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData)); // 수신 데이터를 구조체로 복사

  // 수신된 데이터 출력
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("ID: ");
  Serial.println(myData.id);
  Serial.print("Speed: ");
  Serial.println(myData.speed);
  Serial.print("Angle: ");
  Serial.println(myData.angle);
}

void setup() {
  Serial.begin(115200);  // 시리얼 통신 시작

  pinMode(Led_1, OUTPUT);  // LED 1 출력 모드
  pinMode(Led_2, OUTPUT);  // LED 2 출력 모드
  
  // Wi-Fi 초기화
  WiFi.mode(WIFI_STA);

  // ESP-NOW 초기화
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    digitalWrite(Led_1, LOW);
    digitalWrite(Led_2, HIGH);
    return;
  } else {
    Serial.println("ESP-NOW Initialized");
    digitalWrite(Led_1, HIGH);
    digitalWrite(Led_2, LOW);
  }

  // 수신 콜백 함수 등록
  esp_now_register_recv_cb(onReceive);
}

void loop() {
  // 수신기는 수신 대기 상태
}
