#include <esp_now.h>
#include <WiFi.h>

// Definitions for ESP NOW functions start---------------------------------------------------*

// Transmission callback function
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
   if (status == ESP_NOW_SEND_SUCCESS) {
      Serial.println("Successfully sent");
   } else {
      Serial.println("Failed to send");
   }
}

// Reception callback function
void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len) {
  Serial.print("Data received: ");
  Serial.println((char)data[0]);
}

// Definitions for ESP NOW functions end---------------------------------------------------*

// Preprocessing for ESP NOW --------------------------------------------------------------*
#define btn1 18
#define btn2 19
const int ledPin = 2; // LED pin configuration
unsigned long lastMsgTime = 0;

// MAC addresses for this board and the peer board
byte boardA[] = {0x00,0x00,0x00,0x00,0x00,0x00};
byte boardB[] = {0x00,0x00,0x00,0x00,0x00,0x00};
esp_now_peer_info_t dest;

// Preprocessing for ESP NOW end ---------------------------------------------------------*

// Preprocessing for Wi-Fi start ---------------------------------------------------------*

// Input your network information
const char* ssid = "Hi";
const char* password = "htrewi234@";

// Create a server
WiFiServer server(80);

// Track the LED state to maintain consistency
bool ledState = false;

// Preprocessing for Wi-Fi end -----------------------------------------------------------*

void setup() {
  Serial.begin(115200);
  
  // Setup function for ESP NOW start ----------------------------------------------------*
  pinMode(btn1, INPUT_PULLUP);
  pinMode(btn2, INPUT_PULLUP);

  // Set Wi-Fi mode to station mode
  WiFi.mode(WIFI_STA);

  // Start ESP NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Failed to start ESPNOW");
    while (true); // Stop if ESP NOW fails to start
  } else {
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

  // Setup function for ESP NOW end ------------------------------------------------------*

  // Setup function for Wi-Fi start ------------------------------------------------------*
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  int wifiRetryCount = 0;
  while (WiFi.status() != WL_CONNECTED && wifiRetryCount < 20) {
    delay(500);
    Serial.print(".");
    wifiRetryCount++;
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Failed to connect to WiFi");
    while (true); // Stop if Wi-Fi connection fails
  }

  Serial.println("");
  Serial.println("Connected to WiFi.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Start the server
  server.begin();
  // Setup function for Wi-Fi end -------------------------------------------------------*
}

void loop() {
  WiFiClient client = server.available();   // Wait for client requests

  if (client) {                             // When a new client connects
    Serial.println("New client connected.");   // Print a message to the serial port
    String currentLine = "";                // String to hold incoming data from the client
    bool requestHandled = false;            // Track whether the request has been handled

    while (client.connected()) {            // While the client is connected
      if (client.available()) {             // If there is data available to read from the client
        char c = client.read();             // Read the data
        Serial.write(c);                    // Print it to the serial monitor
        if (c == '\n') {                    // If the character is a newline

          // If the current line is empty, it indicates the end of the HTTP request
          if (currentLine.length() == 0) {
            // HTTP header response
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // HTML content
            client.println("<!DOCTYPE html>");
            client.println("<html lang=\"ko\">");
            client.println("<head>");
            client.println("<meta charset=\"UTF-8\">");
            client.println("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">");
            client.println("<title>On/Off Buttons</title>");
            client.println("<style>");
            client.println(".btn { width: 100px; height: 50px; border: none; border-radius: 10px; cursor: pointer; font-size: 18px; color: white; margin: 10px; transition: opacity 0.3s; }");
            client.println(".btn-on { background-color: red; }");
            client.println(".btn-off { background-color: green; }");
            client.println(".disabled { opacity: 0.5; cursor: not-allowed; }");
            client.println("</style>");
            client.println("</head>");
            client.println("<body>");
            if (ledState) {
              client.println("<button id=\"onBtn\" class=\"btn btn-on disabled\">ON</button>");
              client.println("<button id=\"offBtn\" class=\"btn btn-off\" onclick=\"location.href='/off'\">OFF</button>");
            } 
            else {
              client.println("<button id=\"onBtn\" class=\"btn btn-on\" onclick=\"location.href='/on'\">ON</button>");
              client.println("<button id=\"offBtn\" class=\"btn btn-off disabled\">OFF</button>");
            }
            client.println("</body>");
            client.println("</html>");

            // HTTP response must end with a blank line
            client.println();
            requestHandled = true;  // Indicate that the request has been handled
            break;
          } 
          else { // If the character is not a newline, add it to currentLine
            currentLine = "";
          }
        } 
        else if (c != '\r') {  // If the character is not a carriage return
          currentLine += c;      // Add it to currentLine
        }

        // Check if the client's request is "GET /on" or "GET /off"
        if (!requestHandled && currentLine.endsWith("GET /on")) {
          digitalWrite(ledPin, HIGH);               // Turn on the LED

          byte data = '0';
          esp_now_send(dest.peer_addr, &data, sizeof(data)); // Send a message once when the button is pressed
          lastMsgTime = millis();                           // Update the last message sent time
          ledState = true;                                  // Update the state
          requestHandled = true;                            // Indicate that the request has been handled
        }
        if (!requestHandled && currentLine.endsWith("GET /off")) {
          digitalWrite(ledPin, LOW);                // Turn off the LED

          byte data = '1';
          esp_now_send(dest.peer_addr, &data, sizeof(data)); // Send a message once when the button is pressed
          lastMsgTime = millis();                            // Update the last message sent time
          ledState = false;                                 // Update the state
          requestHandled = true;                             // Indicate that the request has been handled
        }
      }
    }
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
  }

  // Block for periodic tasks
  unsigned long currentMillis = millis();
  if (currentMillis - lastMsgTime >= 1000) {  // Check periodically every second
    // Perform necessary periodic tasks
    lastMsgTime = currentMillis;
  }
}
