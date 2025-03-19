#include <esp_now.h>
#include <WiFi.h>

#define RELAY_PIN 6
#define LED_PIN 40 // LED pin number

// Timer value for sending messages at regular intervals
unsigned long t = 0;

// Data to be transmitted (bool value)
bool sendData = false; // or true

// MAC address of the peer
byte peerMAC[] = {0xB8, 0xD6, 0x1A, 0xA7, 0x2F, 0xD0};
esp_now_peer_info_t dest;

// Variables to track the success of transmission and reception
bool sendSuccess = false;
bool receiveSuccess = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);

  // Set Wi-Fi mode to Station mode
  WiFi.mode(WIFI_STA);

  // Initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW initialization failed!");
    return;
  }

  // Set up peer device address
  memcpy(dest.peer_addr, peerMAC, sizeof(peerMAC));
  dest.channel = 0; // Use current Wi-Fi channel
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
    Serial.println("Sent data: " + String(sendData ? "true" : "false"));
  }
  
  // Turn on LED if both transmission and reception are successful
  if (sendSuccess && receiveSuccess) {
    digitalWrite(LED_PIN, HIGH);
    sendData = true;
    esp_now_send(dest.peer_addr, (uint8_t *)&sendData, sizeof(sendData));
  } else {
    digitalWrite(LED_PIN, LOW);
    sendData = false;
    esp_now_send(dest.peer_addr, (uint8_t *)&sendData, sizeof(sendData));
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
    if (receivedData == true){
      digitalWrite(RELAY_PIN, HIGH);
    }
    else if (receivedData == 0){
      digitalWrite(RELAY_PIN, LOW);
    }
    receiveSuccess = true; // Successful reception

    // Change LED state based on received data (e.g., turn on LED when true)
    // digitalWrite(LED_PIN, receivedData ? HIGH : LOW); // This line is not needed
  } else {
    Serial.println("Received data length error!");
    receiveSuccess = false; // Failed reception
  }
}
