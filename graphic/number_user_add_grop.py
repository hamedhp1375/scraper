import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class UserCountDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👥 تعداد کاربران برای افزودن")
        self.resize(400, 150)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # متن راهنما
        self.label = QLabel("تعداد کاربرانی که می‌خواهید اضافه کنید را وارد کنید:")
        layout.addWidget(self.label)

        # ورودی عدد
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("مثلاً 50")
        layout.addWidget(self.count_input)

        # دکمه تأیید
        self.btn_confirm = QPushButton("تأیید")
        layout.addWidget(self.btn_confirm)

        # متغیر ذخیره عدد
        self.user_count = None

        # اتصال دکمه
        self.btn_confirm.clicked.connect(self.confirm_and_exit)

    def confirm_and_exit(self):
        """وقتی دکمه تأیید زده شود، عدد ذخیره شده و برنامه بسته می‌شود"""
        value = self.count_input.text().strip()
        if value.isdigit():
            self.user_count = int(value)
            print(f"✅ تعداد کاربران: {self.user_count}")
            QApplication.quit()  # بستن کل برنامه
        else:
            QMessageBox.warning(self, "خطا", "لطفاً فقط عدد وارد کنید.")


# ✅ تست مستقل
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserCountDialog()
    window.show()
    app.exec()
    print("👥 تعداد کاربران انتخاب‌شده:", window.user_count)
