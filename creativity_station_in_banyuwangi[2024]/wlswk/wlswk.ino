#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <SPIFFS.h>


const char* ssid = "Hi";
const char* password = "htrewi234@";

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);

  // Initialize SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("An Error has occurred while mounting SPIFFS");
    return;
  }

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to Wi-Fi");

  // Serve files from SPIFFS
  server.serveStatic("/", SPIFFS, "/").setDefaultFile("index.html");

  // Handle on/off button requests
  server.on("/on", HTTP_GET, [](AsyncWebServerRequest *request){
    // Handle the ON request
    digitalWrite(LED_BUILTIN, HIGH);
    request->send(200, "text/plain", "LED is ON");
  });

  server.on("/off", HTTP_GET, [](AsyncWebServerRequest *request){
    // Handle the OFF request
    digitalWrite(LED_BUILTIN, LOW);
    request->send(200, "text/plain", "LED is OFF");
  });
  
  Serial.println("IP address: ");
  // WiFi에 연결이되고 DHCP로 IP를 받아오면 WiFi.localIP()확인할 수 있다.
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  // Nothing to do here
}
