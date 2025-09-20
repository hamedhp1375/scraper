# simple_pyqt6_app.py
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QGridLayout, QWidget

from logic.login import LoginGraphic


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سلام از PyQt6")
        self.resize(500, 400)
        self.move(100, 100)
        self.grid = QGridLayout()

        self.profilePathInput = QLineEdit()
        self.profilePathInput.setPlaceholderText("Hi")

        self.profilePathInput2 = QLineEdit()
        self.profilePathInput2.setPlaceholderText("Hi2")

        self.grid.addWidget(self.profilePathInput, 0, 0)
        self.grid.addWidget(self.profilePathInput2, 1, 0)

        self.btn_start = QPushButton("Start")
        self.grid.addWidget(self.btn_start, 2, 0)

        # login_g = LoginGraphic(driver)
        # if is_login:
        #     phone = ""
        #     self.enter_phone = QLineEdit()
        #     self.grid.addWidget(self.enter_phone, 3, 0)
        #     phone =111

        #     After do delete that from layout
        #     self.code = QLineEdit()
        #     self.grid.addWidget(self.code, 4, 0)


        self.setLayout(self.grid)


        # self.setCentralWidget(QLabel("سلام دنیا!"))


    def login(self):
        self.label = QLabel("شماره خود را وارد کنید")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("اینجا بنویس...")
        self.button = QPushButton("ارسال شماره تلفن")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())



