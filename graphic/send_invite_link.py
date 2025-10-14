import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class LinkInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📨 وارد کردن لینک دعوت")
        self.resize(400, 150)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # متن توضیحی
        self.label = QLabel("لطفاً لینک دعوت را وارد کنید:")
        layout.addWidget(self.label)

        # ورودی لینک
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("مثلاً https://eitaa.com/joinchat/xxxxxx")
        layout.addWidget(self.link_input)

        # دکمه تأیید
        self.btn_confirm = QPushButton("تأیید")
        layout.addWidget(self.btn_confirm)

        # مقدار لینک نهایی
        self.link = None

        # اتصال دکمه
        self.btn_confirm.clicked.connect(self.get_link)

    def get_link(self):
        """وقتی کاربر روی دکمه کلیک کند مقدار را گرفته و پنجره را می‌بندد"""
        self.link = self.link_input.text().strip()
        print(f"✅ لینک دریافت شد: {self.link}")
        self.close()


# ✅ تست مستقل از فایل
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinkInputWindow()
    window.show()
    app.exec()
    print("🔗 لینک نهایی:", window.link)
