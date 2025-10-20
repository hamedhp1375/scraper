from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication
import sys


class LinkInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ورود لینک")
        self.resize(400, 150)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # برچسب
        self.label = QLabel("لینک ذعوت مورد نظر را وارد کنید:")
        layout.addWidget(self.label)

        # ورودی لینک
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("https://example.com/...")
        layout.addWidget(self.link_input)

        # دکمه تأیید
        self.btn_ok = QPushButton("تأیید")
        self.btn_ok.clicked.connect(self.submit_link)
        layout.addWidget(self.btn_ok)

        # مقدار نهایی لینک
        self.link = None

    def submit_link(self):
        """وقتی کاربر روی دکمه کلیک کرد، لینک رو ذخیره و پنجره بسته میشه"""
        self.link = self.link_input.text()
        self.close()



