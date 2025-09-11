import socket
import threading
from typing import Dict, Tuple


class ChatServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 5000) -> None:
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients: Dict[socket.socket, str] = {}
        self.lock = threading.Lock()

    def start(self) -> None:
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(10)
        print(f"[서버] {self.host}:{self.port} 에서 대기 중…")
        try:
            while True:
                conn, addr = self.server_sock.accept()
                th = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                th.start()
        except KeyboardInterrupt:
            print('\n[서버] 종료 신호 감지. 서버를 정리합니다…')
        finally:
            self.shutdown()

    def handle_client(self, conn: socket.socket, addr: Tuple[str, int]) -> None:
        conn.settimeout(600)
        try:
            name = self._recv_line(conn)
            if not name:
                conn.close()
                return

            with self.lock:
                self.clients[conn] = name
            self.broadcast(f'{name}님이 입장하셨습니다.')

            # 사용자 메시지 루프
            while True:
                msg = self._recv_line(conn)
                if msg is None:
                    break
                text = msg.strip()
                if text == '/종료':
                    self._safe_send(conn, '연결을 종료합니다.')
                    break

                # === 귓속말 기능 추가 ===
                if text.startswith('/w '):
                    parts = text.split(' ', 2)
                    if len(parts) < 3:
                        self._safe_send(conn, '[서버] 사용법: /w 대상유저 메시지')
                        continue
                    target_name, whisper_msg = parts[1], parts[2]
                    self.send_whisper(conn, name, target_name, whisper_msg)
                else:
                    if text:
                        self.broadcast(f'{name}> {text}')
        except (ConnectionResetError, ConnectionAbortedError, socket.timeout):
            pass
        finally:
            # 정리 및 퇴장 안내
            with self.lock:
                name = self.clients.pop(conn, None)
            try:
                conn.close()
            except Exception:
                pass
            if name:
                self.broadcast(f'{name}님이 퇴장하셨습니다.')

    def send_whisper(self, sender_conn: socket.socket, sender_name: str, target_name: str, message: str) -> None:
        target_conn = None
        with self.lock:
            for conn, uname in self.clients.items():
                if uname == target_name:
                    target_conn = conn
                    break

        if target_conn:
            whisper_text = f"[귓속말] {sender_name} → {target_name}: {message}"
            self._safe_send(target_conn, whisper_text)
            self._safe_send(sender_conn, whisper_text)  # 보낸 사람도 확인 가능하게
        else:
            self._safe_send(sender_conn, f"[서버] 대상 유저 '{target_name}' 를 찾을 수 없습니다.")

    def broadcast(self, message: str) -> None:
        data = (message + '\n').encode('utf-8')
        remove_list = []
        with self.lock:
            for cli in self.clients.keys():
                try:
                    cli.sendall(data)
                except Exception:
                    remove_list.append(cli)
        if remove_list:
            with self.lock:
                for cli in remove_list:
                    self.clients.pop(cli, None)
                    try:
                        cli.close()
                    except Exception:
                        pass

    def _recv_line(self, conn: socket.socket) -> str:
        buffer = []
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                return None
            try:
                part = chunk.decode('utf-8')
            except UnicodeDecodeError:
                part = chunk.decode('utf-8', errors='ignore')
            buffer.append(part)
            if '\n' in part:
                break
        return ''.join(buffer).split('\n', 1)[0]

    def _safe_send(self, conn: socket.socket, message: str) -> None:
        try:
            conn.sendall((message + '\n').encode('utf-8'))
        except Exception:
            pass

    def shutdown(self) -> None:
        with self.lock:
            for cli in list(self.clients.keys()):
                try:
                    cli.close()
                except Exception:
                    pass
            self.clients.clear()
        try:
            self.server_sock.close()
        except Exception:
            pass
        print('[서버] 종료 완료')


if __name__ == '__main__':
    ChatServer(host='0.0.0.0', port=5050).start()