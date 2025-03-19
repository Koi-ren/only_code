#include <WiFi.h>
#include <WebServer.h>

#define LED_PIN 16 // LED 핀 번호

bool sendData = true; // 송신할 bool 데이터

// Set up the AP credentials
const char* ssid = "Hi";
const char* password = "htrewi234@";
String htmlON = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Switch Button - On</title>
    <style>
    body {
        background: rgb(7, 22, 60);
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        overflow: hidden;
        color: #fff;
        text-align: center;
    }

    .background-text {
        font-size: 2.5rem;
        font-weight: bold;
        opacity: 0.5;
        z-index: -1;
        pointer-events: none;
        width: 90%;
        max-width: 800px;
        margin-bottom: 10px;
    }

    .sub-text {
        font-size: 1.2rem;
        opacity: 0.7;
        z-index: 1;
        pointer-events: none;
        width: 90%;
        max-width: 800px;
        margin-bottom: 30px;
    }

    .form-box {
        position: relative;
        margin-top: 50px;
    }

    .button-box {
        width: 220px;
        position: relative;
        border-radius: 30px;
        background: #fff;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: space-between;
    }

    .toggle-label {
        padding: 10px 40px;
        cursor: pointer;
        background: transparent;
        border: 0;
        outline: none;
        position: relative;
        text-align: center;
        z-index: 1;
        font-size: 1rem;
        color: #000;
    }

    #btn {
        position: absolute;
        top: 0;
        left: 0;
        width: 110px;
        height: 100%;
        background: #e6bc22;
        border-radius: 30px;
        transition: .5s;
        z-index: 0;
    }

    .description {
        margin-top: 30px;
        font-size: 1rem;
        opacity: 0.8;
    }
    </style>
</head>
<body>
    <div class="background-text">IoT Based Automatic Pressure Control for Biogas System</div>
    <div class="sub-text">(Kontrol Tekanan Otomatis Berbasis IoT untuk Sistem Biogas)</div>

    <div class="form-box">
        <div class="button-box">
            <div id="btn"></div>
            <label class="toggle-label" onclick="location.href='/off'">Off</label>
            <label class="toggle-label" onclick="location.href='/on'">On</label>
        </div>
    </div>

    <div class="description">Pompa Biogas On.</div>
</body>
</html>
  )rawliteral";

String htmlOFF = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Switch Button - Off</title>
    <style>
    body {
        background: rgb(7, 22, 60);
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        overflow: hidden;
        color: #fff;
        text-align: center;
    }

    .background-text {
        font-size: 2.5rem;
        font-weight: bold;
        opacity: 0.5;
        z-index: -1;
        pointer-events: none;
        width: 90%;
        max-width: 800px;
        margin-bottom: 10px;
    }

    .sub-text {
        font-size: 1.2rem;
        opacity: 0.7;
        z-index: 1;
        pointer-events: none;
        width: 90%;
        max-width: 800px;
        margin-bottom: 30px;
    }

    .form-box {
        position: relative;
        margin-top: 50px;
    }

    .button-box {
        width: 220px;
        position: relative;
        border-radius: 30px;
        background: #fff;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: space-between;
    }

    .toggle-label {
        padding: 10px 40px;
        cursor: pointer;
        background: transparent;
        border: 0;
        outline: none;
        position: relative;
        text-align: center;
        z-index: 1;
        font-size: 1rem;
        color: #000;
    }

    #btn {
        position: absolute;
        top: 0;
        left: 0;
        width: 110px;
        height: 100%;
        background: #e6bc22;
        border-radius: 30px;
        transition: .5s;
        z-index: 0;
    }

    .description {
        margin-top: 30px;
        font-size: 1rem;
        opacity: 0.8;
    }
    </style>
</head>
<body>
    <div class="background-text">IoT Based Automatic Pressure Control for Biogas System</div>
    <div class="sub-text">(Kontrol Tekanan Otomatis Berbasis IoT untuk Sistem Biogas)</div>

    <div class="form-box">
        <div class="button-box">
            <div id="btn"></div>
            <label class="toggle-label" onclick="location.href='/off'">Off</label>
            <label class="toggle-label" onclick="location.href='/on'">On</label>
        </div>
    </div>

    <div class="description">Pompa Biogas Off.</div>
</body>
</html>
  )rawliteral";

// Create a WebServer object that listens on port 80
WebServer server(80);

// Function to handle the root URL "/"
void handleRoot() {
  
  server.send(200, "text/html", htmlOFF);
}

// Function to handle the "On" button press
void handleOn() {
  pumpState = true; // Set pump state to on
  Serial.println("Pump state set to ON");
  server.send(200, "text/html", htmlON);
}

// Function to handle the "Off" button press
void handleOff() {
  pumpState = true; // Set pump state to on
  Serial.println("Pump state set to ON");
  server.send(200, "text/html", htmlOFF);
}

void setup() {
  // Start Serial communication
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, 16, 17); // Serial2 포트 (TX=17, RX=16)
  pinMode(LED_PIN, OUTPUT);

  // Set up the ESP32 as an Access Point
  WiFi.softAP(ssid, password);
  Serial.println("Access Point started");

  // Print the IP address of the ESP32
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.softAPIP());

  // Define the root URL handler
  server.on("/", handleRoot);

  // Define the handlers for the buttons
  server.on("/on", handleOn);
  server.on("/off", handleOff);

  // Start the web server
  server.begin();
  Serial.println("Web server started");
}

void loop() {
  // Continuously handle client requests
  server.handleClient();
  //pumpState ? HIGH : LOW
  delay(2000);
  Serial2.write(pumpState ? 1 : 0);
  Serial.println("board B - sendData: " + String(sendData ? "true" : "false"));

  // 수신된 데이터가 있는 경우 처리
  if (Serial2.available()) {
    char receivedChar = Serial2.read();
    bool receivedData = (receivedChar == '1'); // '1'은 true, '0'은 false로 해석
    if (receivedData == true){
        handleOn;
    }
    else{
        handleOff;
    }    
    Serial.print("board B - receicedData: ");
    Serial.println(receivedData ? "true" : "false");
  }

  WiFiClient client = server.available();

 if (client) {                             // When a new client connects
    Serial.println("New client connected.");   // Print a message to the serial port
    String currentLine = "";                // String to hold incoming data from the client
    bool requestHandled = false;            // Track whether the request has been handled

    while (client.connected()) {            // While the client is connected
      if (client.available()) {             // If there is data available to read from the client
        char c = client.read();             // Read the data
        Serial.write(c)
    }
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
  }
  
}
