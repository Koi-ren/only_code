#include<WiFi.h>


const char* ssid = "";
const char* password = "";
String led ="off";

WiFiServer server(80);
String heder = R"rawltieral(
  <!DOCTYPE html>
    <html>
    <head>
    <meta name = "viewport" content = "width = device-width, initial-scale = 1">
    <link rel = "icon" href = "data:,">
    <style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center}
    .button {background - color: #4CAF50; border: none; color: white; padding; 16px 40px;
    text-decoration: none; font-size: 30px; margin: 2px; cusor: pointer;)
    .button2 {buckground-color: #55555;}</style>
    </head>
    <body>
      <h1>ESP32 Led Controller</h1>)rawliteral";
String foter="</body></html>";

void setup() {
  Serial.begin(11520);
  pinMode(2,OUTPUT);
  Serial.print("connecting to ");
  Serial.print(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("Connected");
  Serial.println("IP Address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if(client){
    Serial.println("New Client.");
    String currentLine = "";
    while(client.connected()){

      if(client.available()){
        char c = client.read();
        Serial.write(c);
        if(c =='\n'){

          if(currentLine.length() ==0){
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            //client.print("Click <a href=\"/H\">here</a> to turn the LED on pin 5 on.<br>");
            //client.print("Click <a href=\"/L\">here</a> to turn the LED on pin 5 off.<br>");
            client.print(header);
            if (led == "off") {
              client.println("<p><a href=\"/H\"<button class =\"button\">ON</button></a></p>");
              }
            else {
              client.println("<p><a href=\"/L\"><button class =\"button button2\">OFF</button></a></p>");
            }
  
            client.print(footer);
            client.println();
            break;
          }
          else{
            currentLine = "";
          }

        }
        else if (c != '\r'){
          currentLine += c;
        }
        if (currentLine.endsWith("GET /H")) {
          digitalWrite(2, HIGH);
          led = "on";
        }
        if (currentLine.endsWith("GET /L")) {
          digitalWrite(2, LOW);
          led = "off";
        }
      }
    }
    client.stop();
    Serial.println("Client Disconnected.");
  }
  delay(20000);
}
