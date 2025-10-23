import csv
import os
import smtplib
import getpass
from typing import List, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailSender:
    """메일 발송을 담당하는 클래스(CapWord 명명)."""

    def __init__(self, provider: str, sender_email: str, password: str):
        """
        provider: 'gmail' 또는 'naver'
        """
        self.sender_email = sender_email
        self.password = password

        if provider.lower() == 'gmail':
            self.smtp_server = 'smtp.gmail.com'
            self.smtp_port = 587
        elif provider.lower() == 'naver':
            self.smtp_server = 'smtp.naver.com'
            self.smtp_port = 587
        else:
            raise ValueError("지원하지 않는 provider 입니다. 'gmail' 또는 'naver' 중 선택하세요.")

    # ---------- 템플릿 ----------

    def render_html(self, name: str) -> Tuple[str, str]:
        """
        HTML/Plain 템플릿을 반환한다.
        - name: 수신자 이름(개인화)
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
          <meta charset="utf-8">
          <title>안내 메일</title>
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; }}
            .wrap {{ max-width: 640px; margin: 24px auto; padding: 24px; border: 1px solid #eee; border-radius: 12px; }}
            h1 {{ margin: 0 0 12px 0; color: #111; font-size: 20px; }}
            p {{ line-height: 1.6; color: #333; }}
            .btn {{ display:inline-block; padding:10px 16px; background:#2563eb; color:#fff; text-decoration:none; border-radius:8px; }}
            .foot {{ margin-top: 20px; font-size: 12px; color: #777; }}
          </style>
        </head>
        <body>
          <div class="wrap">
            <h1>{name}님, 안녕하세요!</h1>
            <p>이메일 테스트 안내 드립니다. HTML 형식으로 작성되었으며
            수신자별로 이름이 개인화되어 전송됩니다.</p>
            <p><a class="btn" href="https://www.naver.com" target="_blank" rel="noreferrer">네이버 바로가기</a></p>
            <p class="foot">본 메일은 과제용 테스트 메일입니다.</p>
          </div>
        </body>
        </html>
        """.strip()

        plain = f"""{name}님, 안녕하세요!

이 메일은 HTML 형식으로 작성되었으며
수신자별로 이름이 개인화되어 전송됩니다.

네이버 바로가기: https://www.naver.com

(본 메일은 과제용 테스트 메일입니다.)
""".strip()

        return html, plain

    # ---------- 메시지 구성 ----------

    def build_message(self, subject: str, to_email: str, html: str, plain: str) -> MIMEMultipart:
        """
        HTML + Plain(대체 본문) multipart/alternative 메시지 생성.
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        part_plain = MIMEText(plain, "plain", "utf-8")
        part_html = MIMEText(html, "html", "utf-8")
        msg.attach(part_plain)
        msg.attach(part_html)
        return msg

    # ---------- 전송 ----------

    def send_personal(self, targets: List[Tuple[str, str]], subject: str) -> None:
        """
        한 명씩(personal) 개별 전송. (개인화에 유리, 스팸 필터에 안전)
        targets: [(이름, 이메일), ...]
        """
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.password)

            success, fail = 0, 0
            for name, email_addr in targets:
                html, plain = self.render_html(name)
                msg = self.build_message(subject, email_addr, html, plain)
                try:
                    server.sendmail(self.sender_email, [email_addr], msg.as_string())
                    print(f"[OK] {name} <{email_addr}> 전송 완료")
                    success += 1
                except smtplib.SMTPException as e:
                    print(f"[FAIL] {name} <{email_addr}> 전송 실패: {e}")
                    fail += 1

            print(f"\n[SUMMARY] 개인 전송: 성공 {success}명 / 실패 {fail}명")

    def send_bcc(self, targets: List[Tuple[str, str]], subject: str) -> None:
        """
        BCC로 한 번에 전송. (속도 유리, 개인화 불가)
        """
        # 대표 수신자(표시용) -> 보통 본인 주소나 'Undisclosed-Recipients' 사용
        display_to = self.sender_email
        names = [n for n, _ in targets]
        emails = [e for _, e in targets]

        # BCC는 헤더에 넣지 않고 실제 수신자 목록으로만 전달
        # 메시지 'To'에는 표시용 주소만 넣는다.
        # 개인화가 불가하므로 이름은 공통 문구로 처리
        html, plain = self.render_html("여러분")
        msg = self.build_message(subject, display_to, html, plain)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            try:
                server.sendmail(self.sender_email, emails, msg.as_string())
                print(f"[OK] BCC 전송 완료 ({len(emails)}명): {', '.join(names[:5])}{' ...' if len(emails) > 5 else ''}")
            except smtplib.SMTPException as e:
                print(f"[FAIL] BCC 전송 실패: {e}")


# ---------- CSV 로더 ----------

def load_targets(csv_path: str) -> List[Tuple[str, str]]:
    """
    CSV 파일에서 (이름, 이메일) 튜플 리스트를 반환한다.
    - 파일 형식: 이름,이메일
    - 헤더(이름,이메일)가 있어도/없어도 동작
    """
    targets: List[Tuple[str, str]] = []
    if not os.path.exists(csv_path):
        print(f"[ERROR] 대상 CSV를 찾을 수 없습니다: {csv_path}")
        return targets

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = [list(map(str.strip, row)) for row in reader if row]

    if not rows:
        return targets

    # 헤더 감지
    if len(rows[0]) >= 2 and rows[0][0] in ("이름", "name") and rows[0][1] in ("이메일", "email", "e-mail"):
        rows = rows[1:]

    for row in rows:
        if len(row) < 2:
            continue
        name, email_addr = row[0], row[1]
        if name and email_addr:
            targets.append((name, email_addr))

    return targets


# ---------- 실행 엔트리 ----------

def main() -> None:
    """
    - CSV: mail_target_list.csv (이름,이메일)
    - 전송 방식: personal(개인 전송) / bcc(한 번에 전송) 택1
    - SMTP: gmail / naver
    """
    print("=== HTML 메일 발송기 ===\n")
    csv_path = "data/mail_target_list.csv"
    targets = load_targets(csv_path)
    if not targets:
        print("[ERROR] 전송 대상이 없습니다. CSV를 확인하세요.")
        return

    provider = input("SMTP 제공자 선택 (gmail/naver) [gmail]: ").strip().lower() or "gmail"
    sender_email = input("발신자 이메일: ").strip()
    password = getpass.getpass("앱 비밀번호(또는 메일 비밀번호): ")
    subject = input("메일 제목: ").strip() or "안내 메일"

    mode = input("전송 방식 선택 (personal/bcc) [personal]: ").strip().lower() or "personal"

    try:
        sender = MailSender(provider, sender_email, password)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    if mode == "bcc":
        sender.send_bcc(targets, subject)
    else:
        sender.send_personal(targets, subject)

    print("\n[DONE] 작업이 완료되었습니다.")


if __name__ == "__main__":
    main()