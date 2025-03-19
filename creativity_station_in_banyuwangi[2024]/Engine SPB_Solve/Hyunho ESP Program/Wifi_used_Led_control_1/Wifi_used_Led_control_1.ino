#include <esp_now.h>
#include <WiFi.h>

//ESP NOW를 위한 함수 정의 시작---------------------------------------------------*

//송신콜백함수 원형:
//void OnDataSent(uint8_t *mac, uint8_t status) {
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
   //status가 0일때 송신 완료!
   if(status == 0){
      Serial.println("성공적으로 송신했음!");
   }else{
      Serial.println("송신 실패!!");
   }
}

//수신콜백함수 원형:
//void OnDataRecv(uint8_t * mac, uint8_t * data, uint8_t len) {
void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len) {
  //data 수신 데이터
  //len 수신한 데이터의 길이
}

//ESP NOW를 위한 함수 정의 끝---------------------------------------------------*
//ESP NOW를 위한 전처리 --------------------------------------------------------*

#define btn1 18
#define btn2 19
//일정한 간격으로 메시지를 전송하기 위한 타이머값
unsigned long t = 0;

//내가 데이터를 보낼 녀석의 MAC주소
//보드A : 78:E3:6D:18:98:98
//보드B : B8:D6:1A:A7:2F:D0

byte boardA[] = {0x78,0xE3,0x6D,0x18,0x98,0x98};
byte boardB[] = {0xB8,0xD6,0x1A,0xA7,0x2F,0xD0};
esp_now_peer_info_t dest;

//ESP NOW를 위한 전처리창 끝 ---------------------------------------------------*
//Wifi를 위한 전처리창 시작 ----------------------------------------------------*

// 자신의 네트워크 정보로 교체하세요.
const char* ssid = "";
const char* password = "";

// 서버 생성
WiFiServer server(80);

// LED 상태를 추적하여 일관성 유지
bool ledState = false;

//Wifi를 위한 전처리창 끝 ------------------------------------------------------*

void setup() {

  Serial.begin(115200);
  
  //ESP NOW를 위한 setup 함수 시작 ---------------------------------------------*
  pinMode(btn1,INPUT_PULLUP); 
  pinMode(btn2,INPUT_PULLUP);
    //제일 처음 할일! 와이파이모드를 스테이션 모드로!
  WiFi.mode(WIFI_STA); 

  //ESPNOW의 기능을 활성화한다!
  if (esp_now_init() != 0) {
    //ESP NOW 시작 실패!
    Serial.println("ESPNOW 실패!");
    return;
  }else{
     //ESP NOW 시작 성공!
     Serial.println("ESPNOW 성공!");
  }

  //상대방 보드 주소를 대입한다!
  for(int i = 0;i<6;i++){
    dest.peer_addr[i] = boardB[i];
  }
  //상대방의 채널을 설정한다!
  dest.channel = 9;  
  dest.encrypt = false;

  //나의 peer를 등록한다!
  esp_now_add_peer(&dest);

  //송신완료 콜백함수 등록
  esp_now_register_send_cb(OnDataSent);

  //수신완료 콜백 함수 등록
  esp_now_register_recv_cb(OnDataRecv);
  //ESP NOW를 위한 setup 함수 끝 ---------------------------------------------*
  //Wifi를 위한 setup 함수 끝 ------------------------------------------------*
  // Wi-Fi 네트워크에 연결
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // 서버 시작
  server.begin();
  //Wifi를 위한 setup 함수 끝 -------------------------------------------------*
}

void loop() {
  WiFiClient client = server.available();   // 클라이언트 요청 대기

  if (client) {                             // 새로운 클라이언트가 연결되면
    Serial.println("New Client.");          // 시리얼 포트에 메시지 출력
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
          byte data = '0';
          esp_now_send(dest.peer_addr, &data, sizeof(data)); //버튼을 1회 누르면 1회 메시지를 전송하겠다!
          delay(300);                                        //과한 리소스 사용 대비
          ledState = true;                                   // 상태 업데이트
          requestHandled = true;                             // 요청이 처리되었음을 표시
        }
        if (!requestHandled && currentLine.endsWith("GET /off")) {
          byte data = '1';
          esp_now_send(dest.peer_addr, &data, sizeof(data));  //버튼을 1회 누르면 1회 메시지를 전송하겠다!
          delay(300); //이방식은 권장하는 방식은 아님!
          ledState = false;                         // 상태 업데이트
          requestHandled = true;                    // 요청이 처리되었음을 표시
        }
      }
    }
    // 연결 종료
    client.stop();
    Serial.println("Client Disconnected.");
  }
}
