from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
import http.client
import json

PORT = 8080


def get_location_from_ip(ip):
    # 로컬/사설망 구분
    if ip.startswith("127.") or ip.startswith("192.168.") or ip.startswith("10."):
        return "로컬 네트워크"

    try:
        conn = http.client.HTTPSConnection("ipinfo.io")
        conn.request("GET", f"/{ip}/json")
        res = conn.getresponse()

        if res.status == 200:
            data = json.loads(res.read().decode())
            city = data.get("city", "")
            country = data.get("country", "")
            return f"{city}, {country}" if city or country else "위치 정보 없음"
    except Exception as e:
        return f"위치 조회 실패: {e}"

    return "위치 정보 없음"


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # 클라이언트 IP
        client_ip = self.client_address[0]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 위치 조회
        location = get_location_from_ip(client_ip)

        # 접속 로그 출력
        print(f"[접속 로그] 시간: {now}, IP: {client_ip}, 위치: {location}")

        # 200 응답
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # index.html 전송
        try:
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write(
                "<h1>index.html 파일을 찾을 수 없습니다.</h1>".encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), MyHandler)
    print(f"[서버] 0.0.0.0:{PORT} 에서 웹 서버 실행 중...")
    server.serve_forever()
