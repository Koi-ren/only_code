#include <esp_now.h>
#include <WiFi.h>

#define null 15

//Timer value for sending messages at regular intervals
unsigned long t = 0;

char data[] = "This is boardB";

//MAC adress to board
//boardA : 
//board : 

byte boardA[] = {,,,,,};
byte boardB[] = {,,,,,};
esp_now_peer_info_t dest;

void setup() {
  Serial.begin(115200);
  pinMode(null,OUTPUT);

  WiFi.mode(WIFI_STA); 

  //activation ESPNOW
  if (esp_now_init() != 0) {
    Serial.println("ESPNOW Connection failed");
    return;
  }else{
     Serial.println("ESPNOW Conecting successful");
  }

  //using Mac adress by boardA
  for(int i = 0;i<6;i++){
    dest.peer_addr[i] = boardA[i];
  }
  //seting Channel
  dest.channel = 1;  
  dest.encrypt = false;

  //Register the peer
  esp_now_add_peer(&dest);

  //Send complete callback function registration
  esp_now_register_send_cb(OnDataSent);

  //Received callback function registration
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
}

//void OnDataSent(uint8_t *mac, uint8_t status) {
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
   if(status == 0){
      Serial.println("Successfully sent");
   }else{
      Serial.println("Failed to send");
   }
}

//void OnDataRecv(uint8_t * mac, uint8_t * data, uint8_t len) {
void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len) {
  if(data[0] == '0'){
    digitalWrite(null,LOW);
  }else if(data[0] == '1'){
    digitalWrite(null,HIGH);
  }
}