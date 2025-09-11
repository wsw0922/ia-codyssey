import socket
import threading
import sys


class ChatClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 5050) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.alive = True

    def start(self) -> None:
        try:
            self.sock.connect((self.host, self.port))
        except OSError as e:
            print(f'[클라이언트] 서버 접속 실패: {e}')
            return

        recv_thread = threading.Thread(target=self.recv_loop, daemon=True)
        recv_thread.start()

        # 사용자 이름 입력
        name = input('사용자 이름을 입력하세요: ')
        self._send_line(name)

        # 메시지 입력 루프
        try:
            while self.alive:
                text = input()
                self._send_line(text)
                if text.strip() == '/종료':
                    self.alive = False
                    break
        except KeyboardInterrupt:
            self._send_line('/종료')
        finally:
            try:
                self.sock.close()
            except Exception:
                pass
    def recv_loop(self) -> None:
        try:
            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                try:
                    msg = data.decode('utf-8')
                except UnicodeDecodeError:
                    msg = data.decode('utf-8', errors='ignore')
                sys.stdout.write(msg)
                sys.stdout.flush()
        except (ConnectionResetError, ConnectionAbortedError):
            pass
        finally:
            self.alive = False



    def _send_line(self, text: str) -> None:
        try:
            self.sock.sendall((text + '\n').encode('utf-8'))
        except Exception:
            self.alive = False


if __name__ == '__main__':
    # 필요 시 호스트/포트를 수정하여 사용한다.
    ChatClient(host='127.0.0.1', port=5050).start()