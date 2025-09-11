# 시스템 명령줄 인자 처리 및 프로그램 종료를 위한 표준 모듈
import sys

# PyQt5에서 GUI를 구성하는 데 필요한 클래스들 불러오기
from PyQt5.QtWidgets import (
    QApplication,  # PyQt 애플리케이션 객체
    QWidget,       # 기본 창 위젯 (여기서는 계산기 전체 창)
    QPushButton,   # 클릭 가능한 버튼 위젯
    QVBoxLayout,   # 위에서 아래로 쌓는 수직 레이아웃
    QGridLayout,   # 격자 형태의 레이아웃 (버튼 배치용)
    QLineEdit      # 텍스트 입력 또는 출력 위젯 (디스플레이 역할)
)


# 계산기 클래스 정의 (QWidget을 상속받아 GUI 창으로 사용)
class Calculator(QWidget):
    def __init__(self):
        super().__init__()  # QWidget의 생성자 호출 → 윈도우 창 초기화
        self.init_ui()      # 사용자 인터페이스 구성 함수 실행

    def init_ui(self):
        # 디스플레이(숫자 출력창) 생성
        self.display = QLineEdit(self)       # QLineEdit 위젯 생성
        self.display.setReadOnly(True)       # 사용자가 직접 입력하지 못하게 설정 (출력 전용)
        self.display.setStyleSheet(          # 디스플레이에 적용할 스타일 정의
            'font-size: 40px; padding: 10px; margin: 10px;'
        )

        # 전체 레이아웃 생성 (수직 방향: 위에서 아래로 배치)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)           # 디스플레이와 버튼 사이 간격 설정
        main_layout.addWidget(self.display)  # 디스플레이를 메인 레이아웃에 추가

        # 버튼을 배치할 그리드 레이아웃 생성
        grid = QGridLayout()
        grid.setVerticalSpacing(10)          # 버튼 간 세로 간격
        grid.setHorizontalSpacing(10)        # 버튼 간 가로 간격

        # 버튼 텍스트 배열 정의 (아이폰 계산기 순서 기준)
        buttons = [
            ['AC', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+']
        ]

        # 위에서 정의한 버튼 배열을 기반으로 버튼 생성 및 배치
        for row_num, row in enumerate(buttons):             # 행 인덱스와 내용 가져오기
            # 열 인덱스와 버튼 텍스트 가져오기
            for col_num, btn_text in enumerate(row):
                button = QPushButton(btn_text)              # 버튼 위젯 생성
                # 버튼 크기 고정 (가로 × 세로)
                button.setFixedSize(80, 80)
                button.setStyleSheet(                       # 버튼 스타일 지정
                    'font-size: 20px; padding: 10px; margin: 2px;'
                )
                # 버튼 클릭 시 실행할 함수 연결
                # 람다를 사용하여 각 버튼 텍스트를 넘겨주는 방식
                button.clicked.connect(
                    lambda checked, text=btn_text: self.button_clicked(text)
                )
                # 그리드 레이아웃에 버튼을 위치시킴 (행, 열 좌표)
                grid.addWidget(button, row_num, col_num)

        # '0' 버튼은 다른 숫자 버튼보다 가로로 두 칸 넓게 표시해야 함
        zero_button = QPushButton('0')                      # 0 버튼 생성
        zero_button.setFixedSize(170, 80)                   # 가로 크기를 2칸 분량으로 설정
        zero_button.setStyleSheet(
            'font-size: 20px; padding: 10px; margin: 2px;'
        )
        zero_button.clicked.connect(lambda: self.button_clicked('0'))
        # (row=4, col=0) 위치에서 가로 2칸을 차지하도록 배치
        grid.addWidget(zero_button, 4, 0, 1, 2)

        # '.' 버튼 생성 및 배치
        dot_button = QPushButton('.')
        dot_button.setFixedSize(80, 80)
        dot_button.setStyleSheet(
            'font-size: 20px; padding: 10px; margin: 2px;'
        )
        dot_button.clicked.connect(lambda: self.button_clicked('.'))
        grid.addWidget(dot_button, 4, 2)

        # '=' 버튼 생성 및 배치
        equal_button = QPushButton('=')
        equal_button.setFixedSize(80, 80)
        equal_button.setStyleSheet(
            'font-size: 20px; padding: 10px; margin: 2px;'
        )
        equal_button.clicked.connect(lambda: self.button_clicked('='))
        grid.addWidget(equal_button, 4, 3)

        # 그리드 레이아웃을 메인 수직 레이아웃에 추가
        main_layout.addLayout(grid)

        # 메인 레이아웃을 현재 창(계산기 UI)에 적용
        self.setLayout(main_layout)

        # 창 제목 설정
        self.setWindowTitle('아이폰 스타일 계산기')

        # 창 크기 고정 (가로 370px, 세로 550px)
        self.setFixedSize(370, 550)

    # 버튼 클릭 시 실행되는 함수
    def button_clicked(self, text):
        current_text = self.display.text()   # 현재 디스플레이에 표시된 텍스트 가져오기
        new_text = current_text + text       # 새로운 버튼 텍스트를 이어 붙이기
        self.display.setText(new_text)       # 디스플레이에 새로운 텍스트 출력


# 프로그램 실행의 시작점
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  # PyQt5 애플리케이션 객체 생성
        calc = Calculator()           # 계산기 클래스의 인스턴스 생성
        calc.show()                   # 계산기 창 표시
        sys.exit(app.exec_())         # 이벤트 루프 실행 → 창이 닫힐 때까지 대기
    except Exception as e:
        print('예외 발생:', e)        # 예외 발생 시 콘솔에 에러 메시지 출력
