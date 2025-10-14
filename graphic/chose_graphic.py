from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

class MenuBox(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("منوی عملیات")
        self.resize(350, 250)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # متن منو
        menu_text = (
            "===== منو عملیات =====\n"
            "1️⃣ اجرای Add_user_csv\n"
            "2️⃣ اجرای Add_user_to_target_grop\n"
            "3️⃣ ارسال لینک دعوت\n"
            "4️⃣ خروج"
        )

        self.label = QLabel(menu_text)
        layout.addWidget(self.label)

        # فیلد ورودی برای عدد
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("عدد مورد نظر را وارد کنید (1 تا 4)")
        layout.addWidget(self.input_field)

        # دکمه تایید
        self.btn_ok = QPushButton("تأیید")
        self.btn_ok.clicked.connect(self.accept)
        layout.addWidget(self.btn_ok)

        # متغیر برای ذخیره انتخاب
        self.selection = None

    def accept(self):
        """وقتی کاربر تایید می‌زند"""
        value = self.input_field.text().strip()
        if value.isdigit() and int(value) in [1, 2, 3, 4]:
            self.selection = int(value)
            super().accept()
        else:
            self.label.setText("❌ مقدار واردشده معتبر نیست! لطفاً عددی بین 1 تا 4 وارد کنید.")
