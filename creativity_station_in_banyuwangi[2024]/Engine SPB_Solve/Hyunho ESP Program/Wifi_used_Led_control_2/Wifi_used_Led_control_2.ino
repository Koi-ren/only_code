#include <esp_now.h>
#include <WiFi.h>

// ESP NOW를 위한 함수 정의 시작---------------------------------------------------*

// 송신 콜백함수
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
   if (status == ESP_NOW_SEND_SUCCESS) {
      Serial.println("성공적으로 송신했음!");
   } else {
      Serial.println("송신 실패!!");
   }
}

// 수신 콜백함수
void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len) {
  Serial.print("데이터 수신: ");
  Serial.println((char)data[0]);
}

// ESP NOW를 위한 함수 정의 끝---------------------------------------------------*

// ESP NOW를 위한 전처리 --------------------------------------------------------*

#define btn1 18
#define btn2 19
const int ledPin = 2; // LED 핀 설정
unsigned long lastMsgTime = 0;

// 나와 상대방 보드의 MAC 주소
byte boardA[] = {,,,,,};
byte boardB[] = {,,,,,};
esp_now_peer_info_t dest;

// ESP NOW를 위한 전처리 끝 ---------------------------------------------------*

// Wi-Fi를 위한 전처리 시작 ----------------------------------------------------*

// 자신의 네트워크 정보를 입력
const char* ssid = "";
const char* password = "";

// 서버 생성
WiFiServer server(80);

// LED 상태를 추적하여 일관성 유지
bool ledState = false;

// Wi-Fi를 위한 전처리 끝 ------------------------------------------------------*

void setup() {
  Serial.begin(115200);
  
  // ESP NOW를 위한 setup 함수 시작 ---------------------------------------------*
  pinMode(btn1, INPUT_PULLUP);
  pinMode(btn2, INPUT_PULLUP);

  // 와이파이 모드를 스테이션 모드로 설정
  WiFi.mode(WIFI_STA);

  // ESP NOW 시작
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESPNOW 시작 실패!");
    while (true); // ESP NOW 시작 실패 시 멈춤
  } else {
    Serial.println("ESPNOW 시작 성공!");
  }

  // 상대방 보드 주소를 대입한다
  memcpy(dest.peer_addr, boardB, 6);
  dest.channel = 0;
  dest.encrypt = false;

  // 상대방 보드를 peer로 등록
  if (esp_now_add_peer(&dest) != ESP_OK) {
    Serial.println("상대방 등록 실패!");
    return;
  }

  // 송신 콜백함수 등록
  esp_now_register_send_cb(OnDataSent);

  // 수신 콜백 함수 등록
  esp_now_register_recv_cb(OnDataRecv);

  // ESP NOW를 위한 setup 함수 끝 ---------------------------------------------*

  // Wi-Fi를 위한 setup 함수 시작 ---------------------------------------------*
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
    Serial.println("WiFi 연결 실패!");
    while (true); // WiFi 연결 실패 시 멈춤
  }

  Serial.println("");
  Serial.println("WiFi 연결됨.");
  Serial.println("IP 주소: ");
  Serial.println(WiFi.localIP());

  // 서버 시작
  server.begin();
  // Wi-Fi를 위한 setup 함수 끝 -------------------------------------------------*
}

void loop() {
  WiFiClient client = server.available();   // 클라이언트 요청 대기

  if (client) {                             // 새로운 클라이언트가 연결되면
    Serial.println("새 클라이언트 연결됨.");   // 시리얼 포트에 메시지 출력
    String currentLine = "";                // 클라이언트로부터 들어오는 데이터를 저장할 문자열
    bool requestHandled = false;            // 요청이 처리되었는지 여부 추적

    while (client.connected()) {            // 클라이언트가 연결된 동안
      if (client.available()) {             // 클라이언트로부터 읽을 수 있는 데이터가 있으면
        char c = client.read();             // 데이터를 읽고
        Serial.write(c);                    // 시리얼 모니터에 출력
        if (c == '\n') {                    // 만약 줄바꿈 문자라면

          // 현재 줄이 비어 있다면 클라이언트의 HTTP 요청 끝
          if (currentLine.length() == 0) {
            // HTTP 헤더 응답
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // HTML 콘텐츠
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
            } else {
              client.println("<button id=\"onBtn\" class=\"btn btn-on\" onclick=\"location.href='/on'\">ON</button>");
              client.println("<button id=\"offBtn\" class=\"btn btn-off disabled\">OFF</button>");
            }
            client.println("</body>");
            client.println("</html>");

            // HTTP 응답은 빈 줄로 끝나야 합니다.
            client.println();
            requestHandled = true;  // 요청이 처리되었음을 표시
            break;
          } else { // 줄바꿈이 아닌 다른 문자가 들어오면 currentLine에 추가
            currentLine = "";
          }
        } else if (c != '\r') {  // 캐리지 리턴 문자가 아니면
          currentLine += c;      // currentLine에 추가
        }

        // 클라이언트 요청이 "GET /on" 또는 "GET /off"인지 확인
        if (!requestHandled && currentLine.endsWith("GET /on")) {
          digitalWrite(ledPin, HIGH);               // LED 켜기

          byte data = '0';
          esp_now_send(dest.peer_addr, &data, sizeof(data)); // 버튼을 1회 누르면 1회 메시지를 전송하겠다!
          lastMsgTime = millis();                           // 마지막 메시지 전송 시간 업데이트
          ledState = true;                                  // 상태 업데이트
          requestHandled = true;                            // 요청이 처리되었음을 표시
        }
        if (!requestHandled && currentLine.endsWith("GET /off")) {
          digitalWrite(ledPin, LOW);                // LED 끄기

          byte data = '1';
          esp_now_send(dest.peer_addr, &data, sizeof(data)); // 버튼을 1회 누르면 1회 메시지를 전송하겠다!
          lastMsgTime = millis();                            // 마지막 메시지 전송 시간 업데이트
          ledState = false;                                  // 상태 업데이트
          requestHandled = true;                             // 요청이 처리되었음을 표시
        }
      }
    }
    // 연결 종료
    client.stop();
    Serial.println("클라이언트 연결 종료.");
  }

  // 정기적인 작업을 위한 코드 블록
  unsigned long currentMillis = millis();
  if (currentMillis - lastMsgTime >= 1000) {  // 1초마다 주기적으로 확인
    // 필요한 정기적 작업 수행
    lastMsgTime = currentMillis;
  }
}
