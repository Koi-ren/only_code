#include <esp_now.h>
#include <WiFi.h>

#define RELAY_PIN 6
#define LED_PIN 16 // LED 핀 번호

// 일정한 간격으로 메시지를 전송하기 위한 타이머 값
unsigned long t = 0;

// 송신할 데이터 (bool 값)
bool sendData = true; // 또는 false

// 상대방의 MAC 주소
byte peerMAC[] = {0xB8, 0xD6, 0x1A, 0xA7, 0x2F, 0xD0};
esp_now_peer_info_t dest;

// 송수신 성공 여부를 추적하는 변수
bool sendSuccess = false;
bool receiveSuccess = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);

  // Wi-Fi 모드를 스테이션 모드로 설정
  WiFi.mode(WIFI_STA);

  // ESP-NOW 기능을 활성화
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESPNOW 초기화 실패!");
    return;
  }

  // 상대방 보드 주소 설정
  memcpy(dest.peer_addr, peerMAC, sizeof(peerMAC));
  dest.channel = 0; // 현재 Wi-Fi 채널 사용
  dest.encrypt = false;

  // 상대방 보드를 피어로 등록
  if (esp_now_add_peer(&dest) != ESP_OK) {
    Serial.println("피어 등록 실패!");
    return;
  }

  // 송신 완료 콜백 함수 등록
  esp_now_register_send_cb(OnDataSent);

  // 수신 콜백 함수 등록
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
  // 2초마다 데이터를 송신
  if (millis() - t > 2000) {
    t = millis();
    sendSuccess = false; // 송신 성공 여부 초기화
    esp_now_send(dest.peer_addr, (uint8_t *)&sendData, sizeof(sendData));
    Serial.println("송신 데이터: " + String(sendData ? "true" : "false"));
  }
  
  // 송수신이 모두 성공하면 LED 켜기
  if (sendSuccess && receiveSuccess) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}

// 송신 콜백 함수
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  if (status == ESP_NOW_SEND_SUCCESS) {
    Serial.println("성공적으로 송신했음!");
    sendSuccess = true; // 송신 성공
  } else {
    Serial.println("송신 실패!");
    sendSuccess = false; // 송신 실패
  }
}

// 수신 콜백 함수
void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len) {
  if (len == sizeof(bool)) {
    bool receivedData = *(bool *)data;
    Serial.print("수신된 데이터: ");
    Serial.println(receivedData ? "true" : "false");
    if (receivedData == true){
      digitalWrite(RELAY_PIN, HIGH);
    }
    else{
        digitalWrite(RELAY_PIN, LOW);
    }
    receiveSuccess = true; // 수신 성공

    // 수신된 데이터에 따라 LED 상태 변경 (예: true일 때 LED 켜기)
    // digitalWrite(LED_PIN, receivedData ? HIGH : LOW); // 이 줄은 필요하지 않음
  } else {
    Serial.println("수신 데이터 길이 오류!");
    receiveSuccess = false; // 수신 실패
  }
}
