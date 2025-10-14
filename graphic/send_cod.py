from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel, QGridLayout

class CodeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("وارد کردن کد")
        self.resize(300, 100)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("کد را وارد کنید:"), 0, 0)
        self.code_input = QLineEdit()
        layout.addWidget(self.code_input, 0, 1)

        btn_send = QPushButton("ارسال کد")
        btn_send.clicked.connect(self.accept)  # accept متد QDialog برای بستن modal
        layout.addWidget(btn_send, 1, 0, 1, 2)

        self.code = None

    def accept(self):
        self.code = self.code_input.text()  # مقدار کد ذخیره میشه
        super().accept()  # پنجره بسته میشه
