#include <esp_now.h>
#include <WiFi.h>

// 일정한 간격으로 메시지를 전송하기 위한 타이머값
unsigned long t = 0;

// 내가 보낼 메시지
char data[] = "나는 boardB보드이다!!";

// 내가 데이터를 보낼 녀석의 MAC주소
// boardA : 0xCC, 0x8D, 0xA2, 0x0C, 0xE0, 0x94
// boardB : 0xCC, 0x8D, 0xA2, 0x0C, 0x29, 0x70

byte boardA[] = {0xCC, 0x8D, 0xA2, 0x0C, 0xE0, 0x94};
byte boardB[] = {0xCC, 0x8D, 0xA2, 0x0C, 0x29, 0x70};
esp_now_peer_info_t dest;

void setup() {
  Serial.begin(115200);
  
  // 제일 처음 할일! 와이파이모드를 스테이션 모드로!
  WiFi.mode(WIFI_STA); 

  // ESPNOW의 기능을 활성화한다!
  if (esp_now_init() != ESP_OK) {
    // ESPNOW 시작 실패!
    Serial.println("ESPNOW 실패!");
    return;
  } else {
    // ESPNOW 시작 성공!
    Serial.println("ESPNOW 성공!");
  }

  // 상대방 보드 주소를 대입한다!
  for (int i = 0; i < 6; i++) {
    dest.peer_addr[i] = boardA[i];
  }
  // 상대방의 채널을 설정한다!
  dest.channel = 1;  
  dest.encrypt = false;

  // 나의 peer를 등록한다!
  esp_now_add_peer(&dest);

  // 송신완료 콜백함수 등록
  esp_now_register_send_cb(OnDataSent);

  // 수신완료 콜백 함수 등록
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (millis() - t > 2000) {
    t = millis();
    // 2초마다 한번씩 하겠다!
    esp_now_send(dest.peer_addr, (uint8_t *) &data, sizeof(data));
  }
}

// 송신콜백함수 원형:
// void OnDataSent(uint8_t *mac, uint8_t status) {
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
   // status가 0일때 송신 완료!
   if (status == ESP_NOW_SEND_SUCCESS) {
      Serial.println("성공적으로 송신했음!");
   } else {
      Serial.println("송신 실패!!");
   }
}

// 수신콜백함수 원형:
// void OnDataRecv(uint8_t * mac, uint8_t * data, uint8_t len) {
void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  String text = "";
  for (int i = 0; i < len; i++) {
    text += (char)data[i];
  }
  Serial.println(text);
}
