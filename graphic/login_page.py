# simple_pyqt6_app.py
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سلام از PyQt6")
        self.setCentralWidget(QLabel("سلام دنیا!"))
        self.resize(800, 600)
        self.move(100, 100)

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



