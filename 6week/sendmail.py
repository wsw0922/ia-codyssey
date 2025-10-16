import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email(sender_email, receiver_email, password, subject, body):
    """    
    Args:
        sender_email (str): 발신자 이메일 주소
        receiver_email (str): 수신자 이메일 주소
        password (str): 발신자 이메일 비밀번호 또는 앱 비밀번호
        subject (str): 이메일 제목
        body (str): 이메일 본문
    """
    # Gmail SMTP 서버 설정
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    # 이메일 메시지 구성
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    
    # 본문 추가
    message.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        # SMTP 서버 연결 및 이메일 전송
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLS 암호화 시작
            server.login(sender_email, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print('이메일이 성공적으로 발송되었습니다!')
            
    except smtplib.SMTPAuthenticationError:
        print('인증 오류: 이메일 주소나 비밀번호를 확인하세요.')
        print('Gmail의 경우 앱 비밀번호를 사용해야 할 수 있습니다.')
    except smtplib.SMTPConnectError:
        print('연결 오류: SMTP 서버에 연결할 수 없습니다.')
        print('인터넷 연결을 확인하세요.')
    except smtplib.SMTPRecipientsRefused:
        print('수신자 오류: 수신자 이메일 주소가 잘못되었습니다.')
    except smtplib.SMTPServerDisconnected:
        print('서버 연결 끊김: SMTP 서버와의 연결이 끊어졌습니다.')
    except smtplib.SMTPException as e:
        print(f'SMTP 오류 발생: {e}')
    except Exception as e:
        print(f'예기치 않은 오류 발생: {e}')


def send_email_with_attachment(sender_email, receiver_email, password, subject, body, attachment_path):
    """
    Args:
        sender_email (str): 발신자 이메일 주소
        receiver_email (str): 수신자 이메일 주소
        password (str): 발신자 이메일 비밀번호 또는 앱 비밀번호
        subject (str): 이메일 제목
        body (str): 이메일 본문
        attachment_path (str): 첨부파일 경로
    """
    # Gmail SMTP 서버 설정
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    # 이메일 메시지 구성
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    
    # 본문 추가
    message.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        # 첨부파일 처리
        if os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            # Base64 인코딩
            encoders.encode_base64(part)
            
            # 첨부파일 헤더 설정
            filename = os.path.basename(attachment_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            message.attach(part)
            print(f'첨부파일 추가됨: {filename}')
        else:
            print(f'경고: 첨부파일을 찾을 수 없습니다: {attachment_path}')
        
        # SMTP 서버 연결 및 이메일 전송
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLS 암호화 시작
            server.login(sender_email, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print('첨부파일이 포함된 이메일이 성공적으로 발송되었습니다!')
            
    except FileNotFoundError:
        print(f'파일 오류: 첨부파일을 찾을 수 없습니다: {attachment_path}')
    except PermissionError:
        print(f'권한 오류: 첨부파일에 접근할 권한이 없습니다: {attachment_path}')
    except smtplib.SMTPAuthenticationError as e:
        print('인증 오류: 이메일 주소나 비밀번호를 확인하세요.')
        print(f'세부 정보: {e}')
        print('Gmail의 경우 앱 비밀번호를 사용해야 할 수 있습니다.')
    except smtplib.SMTPConnectError:
        print('연결 오류: SMTP 서버에 연결할 수 없습니다.')
        print('인터넷 연결을 확인하세요.')
    except smtplib.SMTPRecipientsRefused:
        print('수신자 오류: 수신자 이메일 주소가 잘못되었습니다.')
    except smtplib.SMTPServerDisconnected:
        print('서버 연결 끊김: SMTP 서버와의 연결이 끊어졌습니다.')
    except smtplib.SMTPException as e:
        print(f'SMTP 오류 발생: {e}')
    except Exception as e:
        print(f'예기치 않은 오류 발생: {e}')


def main():
    """
    사용자 입력을 받아 이메일을 전송합니다.
    """
    print('=== SMTP 이메일 전송 프로그램 ===')
    print()
    
    # 사용자 입력 받기
    sender_email = input('발신자 이메일 주소를 입력하세요: ')
    receiver_email = input('수신자 이메일 주소를 입력하세요: ')
    password = input('발신자 이메일 비밀번호(또는 앱 비밀번호)를 입력하세요: ')
    subject = input('이메일 제목을 입력하세요: ')
    body = input('이메일 본문을 입력하세요: ')
    
    # 첨부파일 포함 여부 확인
    while True:
        include_attachment = input('첨부파일을 포함하시겠습니까? (y/n): ').lower().strip()
        if include_attachment in ['y', 'n']:
            break
        else:
            print('올바른 문자를 입력해주세요 (y 또는 n)')
    
    if include_attachment == 'y':
        attachment_path = input('첨부파일 경로를 입력하세요: ')
        send_email_with_attachment(sender_email, receiver_email, password, subject, body, attachment_path)
    else:
        send_email(sender_email, receiver_email, password, subject, body)


if __name__ == '__main__':
    main()