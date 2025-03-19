#include <esp_now.h>
#include <WiFi.h>
#define Led_1 9
#define Led_2 10

// 수신기의 MAC 주소를 설정합니다.
uint8_t receiverAddress1[] = {0x64, 0xE8, 0x33, 0x8B, 0x72, 0x64}; // 수신기 1의 MAC 주소
uint8_t receiverAddress2[] = {0x64, 0xE8, 0x33, 0x8B, 0x9D, 0x98}; // 수신기 2의 MAC 주소

typedef struct struct_message {
  int id;
  int speed;
  int angle;
} struct_message;

// 전송할 데이터 구조체 정의
struct_message myData;

void onSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\nLast Packet Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

void setup() {
  Serial.begin(115200);
  
  pinMode(Led_1, OUTPUT);
  pinMode(Led_2, OUTPUT);

  digitalWrite(Led_1, LOW);
  digitalWrite(Led_2, LOW);
  
  
  // Wi-Fi 초기화
  WiFi.mode(WIFI_STA);

  // ESP-NOW 초기화
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // 송신 콜백 함수 등록
  esp_now_register_send_cb(onSent);

  // 수신기 1 등록
  esp_now_peer_info_t peerInfo1;
  memcpy(peerInfo1.peer_addr, receiverAddress1, 6);
  peerInfo1.channel = 0;  
  peerInfo1.encrypt = false;

  if (esp_now_add_peer(&peerInfo1) != ESP_OK) {
    Serial.println("Failed to add peer 1");
    return;
  }

  // 수신기 2 등록
  esp_now_peer_info_t peerInfo2;
  memcpy(peerInfo2.peer_addr, receiverAddress2, 6);
  peerInfo2.channel = 0;
  peerInfo2.encrypt = false;

  if (esp_now_add_peer(&peerInfo2) != ESP_OK) {
    Serial.println("Failed to add peer 2");
    return;
  }
}

void loop() {
  // 전송할 데이터 생성
  myData.id = 1;
  myData.speed = 50;
  myData.angle = 80;

  // 수신기 1로 데이터 전송
  esp_err_t result1 = esp_now_send(receiverAddress1, (uint8_t *) &myData, sizeof(myData));

  if (result1 == ESP_OK) {
    Serial.println("Sent to Receiver 1 successfully");
  } else {
    Serial.println("Error sending to Receiver 1");
  }

  // 수신기 2로 데이터 전송
  esp_err_t result2 = esp_now_send(receiverAddress2, (uint8_t *) &myData, sizeof(myData));

  if (result2 == ESP_OK) {
    Serial.println("Sent to Receiver 2 successfully");
  } else {
    Serial.println("Error sending to Receiver 2");
  }

  // LED 상태 변경
  if(result1 == ESP_OK && result2 == ESP_OK) {
    digitalWrite(Led_1, HIGH);
    digitalWrite(Led_2, LOW);
  } else {
    digitalWrite(Led_1, LOW);
    digitalWrite(Led_2, HIGH);
  }

  delay(100);
}
