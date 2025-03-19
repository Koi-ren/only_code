// ESP WebServer AJAX(STA Mode)

// AJAX(Asynchronous JavaScript and XML)를 이용하여
// Web page가 Load된 후에 비 동기적으로 Web server에 Data를 보내고,
// Web server로 부터 Data를 읽어서 전체 Page를 Reload 하지 않고,
// Web page를 Update 한다.
// Web page 전체를 Reload 하지 않기 때문에 HTML 문서를 R"(Raw strings)으로
// 저장 할 수 있다. 그 결과 HTML 문서 작성이 용이하고 읽기 쉽다.
// 실시간으로 자주 Web page 내의 일부 Data를 Server로 부터 전달 받아 표시하는 경우 유리하다. 
String header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
// R" : C++ 11 부터 \n 과 같은 Escape character를 처리하지 말고 Raw strings으로 사용 함을 표시
String html_1 = R"=====(
<!DOCTYPE html>
<html>
 <head>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <meta charset='utf-8'>
  <title>ESP Web AJAX</title>
  <style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
   body{margin-top: 30px;} h2 {color: #444444;margin: 30px auto 24px;} h3 {color: #1abc9c;margin-bottom: 20px;}
   .button {display: block;width: 150px;background-color: #1abc9c;border: none;color: white;padding: 8px 12px;text-decoration: none;font-size: 14px;margin: 0px auto 20px;cursor: pointer;border-radius: 4px;}
   .button-s1 {background-color: #34495e;}
   .button-s1:active {background-color: #16a085;}
   .button-s1:hover {background-color: #16a085;}
   p {font-size: 14px;color: #888;margin-bottom: 10px;}
   p.data {line-height: 0.5;}
   .label {line-height: 0.5;}

   #time_P { margin: 10px 0px 15px 0px;}
   table {margin:auto; text-align:center;}
  </style>
 </head>

  <script> 
    let flagLED1 = false;
    let flagLED2 = false;

    // 현재 시간을 표시하는 함수이다. 이 함수는 주기적으로(보통 1초) 실행된다.
  function updateTime() 
    {  
       var d = new Date();
       var t = "";
       t = d.toLocaleTimeString();
       document.getElementById('Time').innerHTML = t;
    }

  // Web page에 주기적으로 Update 할 Data를 Server로 부터 갖어 오기 위한 함수 이다. 
  function getStatus() 
    {  
      ajaxLoad('getStatus');
    }

  // XMLHttpRequest는 현재 사용하는 거의 모든 Browser에 Built-in 되어있는
  // Server로 부터 Data를 Request 하는 object 이다.
  // 주: Internet Explorer old versions(IE5 and IE6)은 지원하지 않는다.
  // XMLHttpRequest는 아래 기능을 가능하게 한다.
  //   Web page를 Reloading 하지 않고 Web page를 Update 할 수 있게 한다.
  //   Web page가 Load된 다음에 Server로 부터 Data를 Requeset 할 수 있다.
  //   Web page가 Load된 다음에 Server로 부터 Data를 Receive 할 수 있다.
  //   Background에서 Server에 Data를 보낼 수 있다.
  var ajaxRequest =new XMLHttpRequest();
 
  // Web server에 URL path(ajaxURL)를 GET Method로 보내고 결과를 Request 하는 함수
  function ajaxLoad(ajaxURL)
    {
      if(!ajaxRequest){ alert('AJAX is not supported.'); return; }
      // Open method는 request type을 지정한다.
      // Open method 기본형: .open(method, url, async)
      // method: GET or POST method를 사용 할 수 있다. 여기서는 GET Method를 사용 한다.
      // url: Server의 (file) Location. 이 프로그램에서는 이 문자열을 명령으로 사용한다.
      // async: true (asynchronous) or false (synchronous)
      // Server에 request를 전송하는 것은 .send() Method를 사용한다.
      ajaxRequest.open('GET',ajaxURL,true);

      // onreadystatechange Property는 XMLHttpRequest 객체의 상태가 변경 될 때마다 실행될 함수를 지정한다.
      ajaxRequest.onreadystatechange = function()
      {
        // readyState property가 4이고 status property가 200이면 응답이 준비된 상태이다.
        if(ajaxRequest.readyState == 4 && ajaxRequest.status==200)
        {
          // Response text를 ajaxResult 변수에 저장한다.
          var ajaxResult = ajaxRequest.responseText;
          // 문자열 변수 ajaxResult 내의 문자를 "|" 문자로 분리하여 Array 변수에 저장한다.
          var commandArray = ajaxResult.split("|");
          // commandArray[0]의 문자열이 'command' 인 경우 commandArray[1]에 따라 Web page에 표시 한다.
          if(commandArray[0] == 'command') {
            if(commandArray[1] == 'LED1On') {
              flagLED1 = true;
              document.getElementById('LED1Control').style.background = '#1abc9c'
              document.getElementById('LED1Control').innerText = 'LED1 Off';
            }
            if(commandArray[1] == 'LED1Off') {
              flagLED1 = false;
              document.getElementById('LED1Control').style.background = '#34495e'
              document.getElementById('LED1Control').innerText = 'LED1 On';
            }
            if(commandArray[1] == 'LED2On') {
              flagLED2 = true;
              document.getElementById('LED2Control').style.background = '#1abc9c'
              document.getElementById('LED2Control').innerText = 'LED2 Off';
            }
            if(commandArray[1] == 'LED2Off') {
              flagLED2 = false;
              document.getElementById('LED2Control').style.background = '#34495e'
              document.getElementById('LED2Control').innerText = 'LED2 On';
            }
            document.getElementById('commandMseg').innerHTML = commandArray[1];
          }
          // commandArray[0]의 문자열이 'status' 인 경우 commandArray[i]의 내용을 Web page에 표시 한다.
          if(commandArray[0] == 'status') {
            if(commandArray[1] == 'LED1On') {
              flagLED1 = true;
              document.getElementById('LED1Control').style.background = '#1abc9c'
              document.getElementById('LED1Control').innerText = 'LED1 Off';
            }
            if(commandArray[1] == 'LED1Off') {
              flagLED1 = false;
              document.getElementById('LED1Control').style.background = '#34495e'
              document.getElementById('LED1Control').innerText = 'LED1 Off';
            }
            if(commandArray[2] == 'LED2On') {
              flagLED2 = true;
              document.getElementById('LED2Control').style.background = '#1abc9c'
              document.getElementById('LED2Control').innerText = 'LED2 Off';
            }
            if(commandArray[2] == 'LED2Off') {
              flagLED2 = false;
              document.getElementById('LED2Control').style.background = '#34495e'
              document.getElementById('LED2Control').innerText = 'LED2 On';
            }
            if(commandArray[3] == 'buttonOn') {
              document.getElementById('ESPStatus').style.background = '#1abc9c'
              document.getElementById('ESPStatus').innerText = 'SW On';
            }
            if(commandArray[3] == 'buttonOff') {
              document.getElementById('ESPStatus').style.background = '#34495e'
              document.getElementById('ESPStatus').innerText = 'SW Off';
            }
            document.getElementById('commandMseg').innerHTML = commandArray[3];
          }
        } 
      }

      // Server에 request를 전송(GET 사용)한다.
      // POST를 사용하는 경우에는 send(string)를 사용한다.
      ajaxRequest.send();
    }

    // LED1의 제어 명령(LED1을 Toggle)를 Server에 전송한다.
    function LED1Control()
    {
      if(flagLED1 == false) {
        ajaxLoad("LED1On");
      }
      else {
        ajaxLoad("LED1Off");    
      }
    }

    // LED2의 제어 명령(LED2을 Toggle)를 Server에 전송한다.
    function LED2Control()
    {
      if(flagLED2 == false) {
        ajaxLoad("LED2On");
      }
      else {
        ajaxLoad("LED2Off");    
      }
    }

    // ESP 보드의 상태를 읽는 명령(URL path)를 Server에 전송한다.
    function getStatus()
    {
      ajaxLoad("getStatus");
    }

    // setInterval: 일정한 주기로 함수(함수 이름만 설정 가능)를 실행 한다.
    // getStatus() 함수를 500mSec 주기로 시행한다. 자주 변경되는 Data 표시에 사용 함. 
//    var myVar1 = setInterval(getStatus, 500);
    // updateTime 함수를 1Sec 주기로 시행한다. 현재 시간 표시에 사용 함.
    var myVar2 = setInterval(updateTime, 1000);  
  </script>
 
<!-- 아래 HTML 문서에 대한 이해는 https://www.w3schools.com/을 참고 요 -->
<body onload="getStatus()">
    <h2>ESP LED Control(STA)</h2>
    <h3 id='commandMseg'>commandMseg</h3>
    <p id="Time" class="data">Time</p>
    <table align='center'>
      <tr>
        <th><button id='LED1Control' class="button button-s1" onclick="LED1Control()">LED1</button></th>
      </tr>
      <tr>
        <th><button id='LED2Control' class="button button-s1" onclick="LED2Control()">LED2</button></th>
      </tr>
      <tr>
        <th><button id='ESPStatus' class="button button-s1" onclick="getStatus()">Button</button></th>
      </tr>
    </table>
 </body>
</html>
)====="; 
 
// ESP32 개발보드를 사용하는 경우 WiFi.h를 사용한다.
#include <WiFi.h>
// ESP8266 개발보드를 사용하는 경우 ESP8266WiFi.h를 사용한다.
//#include <ESP8266WiFi.h>
 
// 본인이 사용하는 공유기(WiFi Router)의 ssid와 psaaword를 설정 한다.
// 본인이 사용하는 공유기의 ssid와 psaaword로 설정 하여야 한다.
#ifndef STA_SSID
#define STA_SSID "REPLACE_WITH_YOUR_SSID"
#define STA_PASSWORD  "REPLACE_WITH_YOUR_PASSWORD"
#endif
 
#define BAUD_LOGGER 115200
#define logger (&Serial)

// 본인이 사용하는 공유기(WiFi Router)의 ssid와 psaaword를 설정 한다.
const char* ssid     = STA_SSID;
const char* password = STA_PASSWORD;

// ESP 개발 보드에 내장된 Button SW(GPIO0)를 사용한다.
const int buttonPin = 0;
// LED 제어에 사용하는 GPIO pins(NodeMcu 보드)
const int LED1pin = 2;
const int LED2pin = 4;
// 개발보드의 상태 전송에 사용하는 문자열 변수
String boardStatus = "";

// WiFiServer Object의 port 번호를 80(HTTP의 Default port)으로 한다.
WiFiServer server(80);
String request = "";
 
void setup() 
{
  logger->begin(BAUD_LOGGER);
  pinMode(LED1pin, OUTPUT);
  pinMode(LED2pin, OUTPUT);
  // LED의 초기 상태를 Off 상태로 설정한다.
  digitalWrite(LED1pin, LOW);
  digitalWrite(LED2pin, LOW);

  logger->println();
  logger->print("Connecting to ");
  logger->println(ssid);
  // SSID 와 password를 사용하여 Wi-Fi network에 연결 한다.
  // STA mode에서 ESP8266은 WIFi Router로 부터 IP Address를 받는다.
  // 이 IP Address를 이용하여 Web server에 접속한다.
  // Internet를 이용하여 외부로 부터 접속하는 경우에는 WIFi Router에 포트포워드 설정을 하여야 한다.
  WiFi.begin(ssid, password);
  // WIFi 연결을 기다린다. 이 동안 Logger에 0.5초 간격으로 . 을 출력 한다.
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    logger->print(".");
  }
  // Local IP address를 출력한다. 이 IP address를 이용하여 Web browser에서 Server에 연결한다.
  logger->println("");
  logger->println("WiFi connected.");
  logger->print("IP address: ");
  logger->println(WiFi.localIP());

  // Server object의 begin method를 call 하여 Server를 시작 한다.
    server.begin();
    logger->println("HTTP server started");
}   // void setup()
 
int findIndex = 0;
char inByte; 
void loop() 
{
    // Client 가 연결되었는지 Check 한다.
    WiFiClient client = server.available();
    // Client 가 연결되지 않은 경우
    if (!client)
    {
    // Function이 return되어 'client' object 가 destroyed 되고 Client는 disconnected 된다.
      return;
    }
    // Client 가 연결된 경우 아래 프로그램을 실행한다.
    else
    {
      // Request의 첫 Line을 읽는다.
      request = client.readStringUntil('\r');
      logger->print("request: ");
      logger->println(request);
      // 만약 Request에 문자열 "getStatus" 가 있으면 개발보드의 상태를 전송한다.
      if ( request.indexOf("getStatus") > 0 )
      { 
        boardStatus = "status|";
        // LED1의 상태를 전송 문자열에 첨부한다.
        // ESP8266은 HIGH일 경우 LED가 Off 되고,
        // ESP32은 HIGH일 경우 LED가 On 된다.
        if (digitalRead(LED1pin) == HIGH) boardStatus += "LED1On|";
        else boardStatus += "LED1Off|";
        // LED2의 상태를 전송 문자열에 첨부한다.
        if (digitalRead(LED2pin) == HIGH) boardStatus += "LED2On|";
        else boardStatus += "LED2Off|";
        // LED1의 상태를 전송 문자열에 첨부한다.
        if (digitalRead(buttonPin) == LOW) boardStatus += "buttonOn";
        else boardStatus += "buttonOff";
        logger->print("Board Status: ");
        logger->println(boardStatus);

        client.print( header );
        // Client에 전송 할 Data를 | 로 구분하여 전송한다.
        client.print( boardStatus );
        // 페이지가 처음 접속되었을 때 방향 표시등의 상태가 표시되기를 원하는 경우 이곳에 코드 삽입 요.
      }
      // Control command 가 수신된 경우
      else if ( request.indexOf("LED1On") > 0 )
      { 
        // ESP8266은 HIGH일 경우 LED가 Off 되고,
        // ESP32은 HIGH일 경우 LED가 On 된다.
        digitalWrite(LED1pin, HIGH);
        // Microcontroller에 Speed up command(U)를 전송한다.
        logger->println("LED1On");
        // Web Browser에 명령 실행 결과를 알리는 메세지를 전송한다.
        client.print( header );
        client.print( "command" );   client.print( "|" );  client.print("LED1On"); 
      }
      else if ( request.indexOf("LED1Off") > 0 )
      { 
        // ESP8266은 LOW일 경우 LED가 On 되고,
        // ESP32은 HIGH일 경우 LED가 Off 된다.
        digitalWrite(LED1pin, LOW);
        logger->println("LED1Off");
        client.print( header );
        client.print( "command" );   client.print( "|" );  client.print("LED1Off"); 
      }
      else if ( request.indexOf("LED2On") > 0 )
      { 
        digitalWrite(LED2pin, HIGH);
        // Microcontroller에 Speed up command(U)를 전송한다.
        logger->println("LED2On");
        // Web Browser에 명령 실행 결과를 알리는 메세지를 전송한다.
        client.print( header );
        client.print( "command" );   client.print( "|" );  client.print("LED2On"); 
      }
      else if ( request.indexOf("LED2Off") > 0 )
      { 
        digitalWrite(LED2pin, LOW);
        logger->println("LED2Off");
        client.print( header );
        client.print( "command" );   client.print( "|" );  client.print("LED2Off"); 
      }
      // Request에서 일치하는 Command를 발견하지 못한 경우 Web page를 전송한다.
      // "ip address/ "로 처음 연결된 경우에도 아래에서 Web page를 전송한다.
      else
      {
        client.flush();
        client.print( header );
        client.print( html_1 ); 
        logger->println("New page served");
      }
    }
} // void loop()