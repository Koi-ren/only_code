#include <esp_now.h>

// Transmission callback function
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
   if (status == ESP_NOW_SEND_SUCCESS) {
      Serial.println("Successfully sent");
   } else {
      Serial.println("Failed to send");
   }
}

// Reception callback function
void OnDataRecv(const esp_now_recv_info *info, const uint8_t *data, int len) {
  Serial.print("Data received: ");
  Serial.println((char)data[0]);
}

#define btn1 18
#define btn2 19
const int ledPin = 2; // LED pin configuration
unsigned long lastMsgTime = 0;

// MAC addresses for this board and the peer board
byte boardA[] = {0x00,0x00,0x00,0x00,0x00,0x00};
byte boardB[] = {0x00,0x00,0x00,0x00,0x00,0x00};
esp_now_peer_info_t dest;

void setup() {
  Serial.begin(115200);
  
  pinMode(btn1, INPUT_PULLUP);
  pinMode(btn2, INPUT_PULLUP);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Failed to start ESPNOW");
    while (true); // Stop if ESP NOW fails to start
  } 
  else {
    Serial.println("Successfully started ESPNOW");
  }

  // Set the peer board address
  memcpy(dest.peer_addr, boardB, 6);
  dest.channel = 9;
  dest.encrypt = false;

  // Register the peer board
  if (esp_now_add_peer(&dest) != ESP_OK) {
    Serial.println("Failed to register peer");
    return;
  }

  // Register the transmission callback function
  esp_now_register_send_cb(OnDataSent);

  // Register the reception callback function
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
  // Example data to send
  uint8_t data = 'A'; // Define the data to send

  //ON
  esp_now_send(dest.peer_addr, &data, sizeof(data));
  //OFF
  esp_now_send(dest.peer_addr, &data, sizeof(data));

  unsigned long currentMillis = millis();
  if (currentMillis - lastMsgTime >= 1000) {  // Check periodically every second
    // Perform necessary periodic tasks
    lastMsgTime = currentMillis;
  }
}
