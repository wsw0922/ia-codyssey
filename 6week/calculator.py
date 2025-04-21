from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,QLineEdit, QPushButton, QGridLayout, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.reset_all()

    # 계산기 초기화

    def reset_all(self):
        # 계산을 위한 변수 초기화
        self.current_value = '0'
        self.operator = None
        self.last_value = None
        self.display.setText('0')

    def initUI(self):
        # 여기서 UI 컴포넌트(버튼, 라벨 등)를 생성하고 배치 설정
        self.setWindowTitle('Calculator')
        self.btn_font = QFont('Arial', 20)

        # 메인 중앙 위젯
        center_witget = QWidget()
        self.setCentralWidget(center_witget)
        center_witget.setStyleSheet("background-color: black;")

        # 전체 레이아웃 (상단 + 버튼 그리드)
        vbox = QVBoxLayout(center_witget)

        # 디스플레이 부분 정의(QLineEdit)
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setText('0')

        # 디스플레이 스타일 적용
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: white;
                border: none;
                font-size: 36px;
                padding: 10px;
            }
        """)

        # 디스플레이 적용
        vbox.addWidget(self.display)

        # 버튼 그리드 설정
        grid = QGridLayout()

        # 버튼 그리드 적용
        vbox.addLayout(grid)

        # 버튼 정의
        buttons = [
            [('AC', 'function'), ('+/-', 'function'),
             ('%', 'function'), ('/', 'operator')],
            [('7', 'number'), ('8', 'number'), ('9', 'number'), ('*', 'operator')],
            [('4', 'number'), ('5', 'number'), ('6', 'number'), ('-', 'operator')],
            [('1', 'number'), ('2', 'number'), ('3', 'number'), ('+', 'operator')],
            [('0', 'number'), ('.', 'number'), ('=', 'operator')]
        ]

        # 버튼 배치 코드
        for row_idx, row_values in enumerate(buttons):
            col_idx = 0
            for val, role in row_values:
                if val is None:
                    col_idx += 1
                    continue
                btn = self.create_button(val, role)
                btn.clicked.connect(self.onButtonClicked)

                # '0' 버튼은 가로 2칸
                if val == '0':
                    grid.addWidget(btn, row_idx, col_idx, 1, 2)
                    col_idx += 2
                else:
                    grid.addWidget(btn, row_idx, col_idx)
                    col_idx += 1

        self.resize(300, 600)

    # 버튼 로직 생성
    def onButtonClicked(self):
        # 클린된 버튼의 객체를 가져오는 메소드 sender()
        btn = self.sender()
        # 버튼에 표시된 텍스트를 얻는 함수
        key = btn.text()

        # 숫자일 경우
        if key.isdigit():
            if self.current_value == '0':
                self.current_value = key
            else:
                self.current_value += key
            self.display.setText(self.current_value)

        # 소수점일 경우
        elif key == '.':
            if '.' not in self.current_value:
                self.current_value += '.'
                self.display.setText(self.current_value)

        # 연산자를 누른경우
        elif key in ['+', '-', '*', '/']:
            self.operator = key
            self.last_value = self.current_value
            self.current_value = '0'
            self.display.setText(self.current_value)

        # '=' 버튼을 누른 경우
        elif key == '=':
            if self.operator and self.last_value is not None:
                result = self.calculate(
                    float(self.last_value),
                    float(self.current_value),
                    self.operator
                )

                # 쉼표 추가한 문자열로 포맷
                if result == int(result):
                    formatted = f"{int(result):,}"
                else:
                    formatted = f"{result:,.10f}".rstrip('0').rstrip('.')

                self.current_value = str(result)
                self.display.setText(formatted)

                # 연속 계산 편의상 last_value에 결과값 저장
                self.last_value = self.current_value

        # 'AC' 버튼을 누른 경우 == 초기화
        elif key == 'AC':
            self.reset_all()

        # '+/-' 버튼을 누른 경우 == 부호 변경
        # startswith 는 문자열 맨 앞이 뭐로 시작하는지 확인 후 boolean 값으로 반환해주는 메소드
        # 만약 -이면 부호를 뺀 나머지를 출력하고
        # 그게 아니라면 -를 붙여서 출력
        elif key == '+/-':
            if self.current_value.startswith('-'):
                self.current_value = self.current_value[1:]
            else:
                self.current_value = '-' + self.current_value
            self.display.setText(self.current_value)

        # '%' 버튼을 누른 경우 퍼센트 계산
        elif key == '%':
            val = float(self.current_value) / 100.0
            self.current_value = str(val)
            self.display.setText(self.current_value)

    # 계산 로직

    def calculate(self, left, right, op):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                return 'Error'
            return left / right
        return 0

    # 버튼 스타일 함수 정의
    def create_button(self, label, role='number'):
        btn = QPushButton(label)

        if label == '0' and role == 'number':
            btn.setFixedSize(170, 80)  # 가로 2칸 정도로
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border: none;
                    border-radius: 40px;
                    font-size: 24px;
                    padding-left: 30px;
                    text-align: left;
                }
                QPushButton:pressed {
                    background-color: #444444;
                }
            """)
        else:
            btn.setFixedSize(80, 80)

            if role == 'number':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #333333;
                        color: white;
                        border: none;
                        border-radius: 40px;
                        font-size: 24px;
                    }
                    QPushButton:pressed {
                        background-color: #444444;
                    }
                """)
            elif role == 'operator':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9500;
                        color: white;
                        border: none;
                        border-radius: 40px;
                        font-size: 24px;
                    }
                    QPushButton:pressed {
                        background-color: #e07e00;
                    }
                """)
            elif role == 'function':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #A5A5A5;
                        color: black;
                        border: none;
                        border-radius: 40px;
                        font-size: 24px;
                    }
                    QPushButton:pressed {
                        background-color: #BBBBBB;
                    }
                """)
        return btn


if __name__ == '__main__':
    app = QApplication([])
    window = Calculator()
    window.show()
    app.exec_()
