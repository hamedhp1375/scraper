import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication, QFileDialog
from graphic.select_file import CSVChooserDialog


class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("انتخاب فایل CSV")
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.btn_open_dialog = QPushButton("انتخاب فایل CSV")
        self.btn_open_dialog.clicked.connect(self.select_file)
        layout.addWidget(self.btn_open_dialog)

        self.file_select = None  # مقدار انتخابی


    def get_selected_file(self):
        """تابع کمکی برای دریافت مقدار انتخاب‌شده"""
        return self.file_select

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "All Files (*.*)"

        )
        print("WE selet file ",file_path)
        if file_path:
            self.file_select=file_path
        else:
            print("error")
# ✅ تست مستقل (وقتی مستقیماً این فایل رو اجرا می‌کنی)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = FileSelector()
    selector.show()
    app.exec()

    # بعد از بستن پنجره، مقدار انتخابی رو چاپ کن
    print("📂 مقدار انتخاب‌شده:", selector.get_selected_file())
