#include <esp_now.h>
#include <WiFi.h>

#define LED_PIN 40 // LED pin number
#define button 36  // button pin number

// Timer value for sending messages at regular intervals
unsigned long t = 0;

// Data to be transmitted (bool values)
bool sendData1 = false; // Signal transmitted and received via ESP NOW
bool sendData2 = false; // Signal transmitted and received via Serial

// MAC address of the peer
byte peerMAC[] = {0xB8, 0xD6, 0x1A, 0xA7, 0x2F, 0xD0};
esp_now_peer_info_t dest;

// Variables to track the success of transmission and reception
bool sendSuccess = false;
bool receiveSuccess = false;

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, 16, 17); // Serial2 port (TX=17, RX=16)
  pinMode(LED_PIN, OUTPUT);
  pinMode(button, INPUT);

  // Set Wi-Fi mode to Station mode
  WiFi.mode(WIFI_STA);

  // Initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW initialization failed!");
    return;
  }

  // Set up peer device address
  memcpy(dest.peer_addr, peerMAC, sizeof(peerMAC));
  dest.channel = 1; // Use current Wi-Fi channel, both devices must be on the same channel
  dest.encrypt = false;

  // Register peer device
  if (esp_now_add_peer(&dest) != ESP_OK) {
    Serial.println("Peer registration failed!");
    return;
  }

  // Register send completion callback function
  esp_now_register_send_cb(OnDataSent);

  // Register receive callback function
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {

  // Send data every 2 seconds
  if (millis() - t > 2000) {
    t = millis();
    sendSuccess = false; // Reset transmission success flag
  }

  if (Serial2.available()) {
    char receivedChar = Serial2.read();
    bool receivedData = (receivedChar == '1');
    sendData1 = receivedData;
    esp_now_send(dest.peer_addr, (uint8_t *)&sendData1, sizeof(sendData1));
    Serial.println("Sent data: " + String(sendData1 ? "true" : "false"));
  }
  
  // Turn on LED if both transmission and reception are successful
  if (sendSuccess && receiveSuccess) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW); 
  }
}

// Send callback function
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  if (status == ESP_NOW_SEND_SUCCESS) {
    Serial.println("Successfully sent!");
    sendSuccess = true; // Successful transmission
  } else {
    Serial.println("Send failed!");
    sendSuccess = false; // Failed transmission
  }
}

// Receive callback function
void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len) {
  if (len == sizeof(bool)) {
    bool receivedData = *(bool *)data;
    Serial.print("Received data: ");
    Serial.println(receivedData ? "true" : "false");
    receiveSuccess = true; // Successful reception

    Serial2.write(sendData2 ? '1' : '0'); // Use updated port
  } 
  else {
    Serial.println("Received data length error!");
    receiveSuccess = false; // Failed reception
  }
}
