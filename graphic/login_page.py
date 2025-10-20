from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
import sys
from graphic.dialog_box_select_file import DialogBox  # فرضی
from logic.login import LoginCLI, LoginGraphic


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ورود اطلاعات و انتخاب فایل")
        self.resize(450, 250)

        layout = QGridLayout()
        self.setLayout(layout)

        # 🔹 دکمه انتخاب فایل
        self.btn_file = QPushButton("انتخاب فایل")
        self.btn_file.clicked.connect(self.select_file)
        layout.addWidget(self.btn_file, 0, 0)

        # 🔹 ورودی شماره
        layout.addWidget(QLabel("شماره خود را وارد کنید:"), 1, 0)
        self.number_input = QLineEdit()
        layout.addWidget(self.number_input, 1, 1)

        # 🔹 ورودی Username
        layout.addWidget(QLabel("Username خود را وارد کنید:"), 2, 0)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input, 2, 1)

        # 🔹 ورودی License
        layout.addWidget(QLabel("License خود را وارد کنید:"), 3, 0)
        self.license_input = QLineEdit()
        layout.addWidget(self.license_input, 3, 1)

        # 🔹 دکمه پایان
        self.btn_ok = QPushButton("تأیید و خروج")
        self.btn_ok.clicked.connect(self.close)
        layout.addWidget(self.btn_ok, 4, 0, 1, 2)

        # 🔹 متغیرها
        self.file_path = None
        self.phone_number = None
        self.username = None
        self.license = None

    def select_file(self):
        dialog = DialogBox()
        self.file_path = dialog.select_file()


    def closeEvent(self, event):
        """وقتی پنجره بسته میشه، مقادیر ورودی‌ها ذخیره می‌شن"""
        self.phone_number = self.number_input.text()
        self.username = self.username_input.text()
        self.license = self.license_input.text()
        event.accept()