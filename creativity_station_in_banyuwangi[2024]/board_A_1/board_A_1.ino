#include <esp_now.h>
#include <WiFi.h>

#define btn1 18
#define btn2 19
//Timer value for sending messages at regular intervals
unsigned long t = 0;

//MAC adress to board
//boardA : 0xCC, 0x8D, 0xA2, 0x0C, 0xE0, 0x94
//boardB : 0xCC, 0x8D, 0xA2, 0x0C, 0x29, 0x70

byte boardA[] = {0xCC, 0x8D, 0xA2, 0x0C, 0xE0, 0x94};
byte boardB[] = {0xCC, 0x8D, 0xA2, 0x0C, 0xE0, 0x94};
esp_now_peer_info_t dest;

void setup() {
  Serial.begin(115200);
  pinMode(btn1,INPUT_PULLUP); 
  pinMode(btn2,INPUT_PULLUP);
  WiFi.mode(WIFI_STA); 

  if (esp_now_init() != 0) {
    Serial.println("ESPNOW Connection failed");
    return;
  }else{
     Serial.println("ESPNOW Conecting successful");
  }

  for(int i = 0;i<6;i++){
    dest.peer_addr[i] = boardB[i];
  }
  dest.channel = 1;  
  dest.encrypt = false;

  esp_now_add_peer(&dest);

  esp_now_register_send_cb(OnDataSent);

  esp_now_register_recv_cb(OnDataRecv);
}
//void OnDataSent(uint8_t *mac, uint8_t status) {
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
   if(status == 0){
      Serial.println("Successfully sent");
   }else{
      Serial.println("Failed to send");
   }

//void OnDataRecv(uint8_t * mac, uint8_t * data, uint8_t len) {
void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len) {
 }
}
void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(btn1) == LOW){
    //button push down
    byte data = '0';
    esp_now_send(dest.peer_addr, &data, sizeof(data));
    //If you press the button once, I'll send you a message once
    delay(300);
  }
  if(digitalRead(btn2) == LOW){
    //button push down
    byte data = '1';
    esp_now_send(dest.peer_addr, &data, sizeof(data));
    //If you press the button once, I'll send you a message once
    delay(300);
  }
}

