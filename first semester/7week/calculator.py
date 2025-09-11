import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.reset()

    def initUI(self):
        self.setWindowTitle("Calculator")
        self.btn_font = QFont("Arial", 20)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: black;")

        vbox = QVBoxLayout(central_widget)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setText('0')
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: white;
                border: none;
                font-size: 36px;
                padding: 10px;
            }
        """)
        vbox.addWidget(self.display)

        grid = QGridLayout()
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

    def reset(self):
        self.current_value = '0'
        self.operator = None
        self.last_value = None
        self.display.setFont(QFont("Arial", 36))
        self.display.setText("0")

    def toggle_sign(self):
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = '-' + self.current_value
        self.display.setText(self.current_value)

    def percent(self):
        val = float(self.current_value) / 100.0
        self.current_value = str(val)
        self.display.setText(self.current_value)

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b

    def divide(self, a, b):
        if b == 0:
            return 'Error: Divide by 0'
        return a / b

    def equal(self):
        if self.operator and self.last_value is not None:
            try:
                a = float(self.last_value)
                b = float(self.current_value)
                if self.operator == '+':
                    result = self.add(a, b)
                elif self.operator == '-':
                    result = self.subtract(a, b)
                elif self.operator == '*':
                    result = self.multiply(a, b)
                elif self.operator == '/':
                    result = self.divide(a, b)

                if isinstance(result, str):  # Error
                    self.display.setText(result)
                    return

                result = round(result, 6)
                formatted = f"{result:,.6f}".rstrip('0').rstrip(
                    '.') if not result == int(result) else f"{int(result):,}"
                font_size = 36 if len(formatted.replace(
                    ',', '')) <= 7 else 28 if len(formatted) <= 10 else 22
                self.display.setFont(QFont("Arial", font_size))
                self.display.setText(formatted)
                self.current_value = str(result)
                self.last_value = self.current_value

            except Exception:
                self.display.setText("Error")

    def onButtonClicked(self):
        key = self.sender().text()
        if key.isdigit():
            if self.current_value == '0':
                self.current_value = key
            else:
                self.current_value += key
            self.display.setText(self.current_value)

        elif key == '.':
            if '.' not in self.current_value:
                self.current_value += '.'
                self.display.setText(self.current_value)

        elif key in ['+', '-', '*', '/']:
            self.operator = key
            self.last_value = self.current_value
            self.current_value = '0'

        elif key == '=':
            self.equal()

        elif key == 'AC':
            self.reset()

        elif key == '+/-':
            self.toggle_sign()

        elif key == '%':
            self.percent()

    def create_button(self, label, role='number'):
        btn = QPushButton(label)
        if label == '0':
            btn.setFixedSize(170, 80)
        else:
            btn.setFixedSize(80, 80)
        btn.setFont(self.btn_font)

        style = """
            QPushButton {
                background-color: %s;
                color: %s;
                border: none;
                border-radius: 40px;
                font-size: 24px;
                %s
            }
            QPushButton:pressed {
                background-color: %s;
            }
        """
        if role == 'number':
            return btn.setStyleSheet(style % ("#333333", "white", "", "#444444")) or btn
        elif role == 'operator' or role == 'equal':
            return btn.setStyleSheet(style % ("#FF9500", "white", "", "#e07e00")) or btn
        elif role == 'function':
            return btn.setStyleSheet(style % ("#A5A5A5", "black", "", "#BBBBBB")) or btn
        return btn


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
