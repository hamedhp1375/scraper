import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from graphic.select_file import CSVChooserDialog


class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("انتخاب فایل CSV")
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.btn_open_dialog = QPushButton("انتخاب فایل CSV")
        self.btn_open_dialog.clicked.connect(self.open_csv_dialog)
        layout.addWidget(self.btn_open_dialog)

        self.selected_file_index = None  # مقدار انتخابی

    def open_csv_dialog(self):
        """پنجره انتخاب فایل رو باز می‌کنه و بعد از انتخاب مقدار رو برمی‌گردونه"""
        dialog = CSVChooserDialog(parent=self)
        if dialog.exec():  # اگر کاربر فایل رو انتخاب کرد
            self.selected_file_index = dialog.selected_index
            print(f"✅ شماره فایل انتخاب‌شده: {self.selected_file_index}")
            self.close()  # 🔹 بستن خود پنجره بعد از انتخاب

    def get_selected_file(self):
        """تابع کمکی برای دریافت مقدار انتخاب‌شده"""
        return self.selected_file_index


# ✅ تست مستقل (وقتی مستقیماً این فایل رو اجرا می‌کنی)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = FileSelector()
    selector.show()
    app.exec()

    # بعد از بستن پنجره، مقدار انتخابی رو چاپ کن
    print("📂 مقدار انتخاب‌شده:", selector.get_selected_file())
