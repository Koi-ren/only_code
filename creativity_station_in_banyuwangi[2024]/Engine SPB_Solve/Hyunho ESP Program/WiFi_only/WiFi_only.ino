#include <WiFi.h>

const char* ssid = "Hi";
const char* password = "htrewi234@";

unsigned long lastMsgTime = 0;

// Create a server
WiFiServer server(80);

// Track the button state to maintain consistency
bool butState = false;

void setup() {
  Serial.begin(115200);
  WiFi.begin(); // Wi-Fi 초기화
  WiFi.mode(WIFI_STA);  //Wi-Fi station 선언
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
            if (butState) {
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
          //digitalWrite(ledPin, HIGH);               // Turn on the LED
          //Serial 통신을 통해서 보낼 데이터 1
          byte data = '0';// Send a message once when the button is pressed
          lastMsgTime = millis();                           // Update the last message sent time
          butState = true;                                  // Update the state
          requestHandled = true;                            // Indicate that the request has been handled
        }
        if (!requestHandled && currentLine.endsWith("GET /off")) {
          //digitalWrite(ledPin, LOW);                // Turn off the LED
          ////Serial 통신을 통해서 보낼 데이터 2
          byte data = '1';
          
          lastMsgTime = millis();                            // Update the last message sent time
          butState = false;                                 // Update the state
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