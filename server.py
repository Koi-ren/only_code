import http.server
import socketserver

class MyCGIHandler(http.server.CGIHTTPRequestHandler):
    cgi_directories = ["/cgi-bin"]  # CGI 스크립트 실행 디렉터리 지정

PORT = 8080  # 원하는 포트 번호

with socketserver.TCPServer(("", PORT), MyCGIHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
