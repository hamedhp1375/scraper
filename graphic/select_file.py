import os
import csv
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QDialog, QListWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QInputDialog, QMessageBox, QWidget, QGridLayout
)

class CSVChooserDialog(QDialog):
    """
    دیالوگی برای نمایش و انتخاب فایل‌های CSV از پوشه مورد نظر.
    بعد از accept شدن، شماره فایل انتخاب‌شده در selected_index قرار می‌گیرد.
    """
    def __init__(self, folder="../result_scraper", parent=None):
        super().__init__(parent)
        self.folder = os.path.abspath(folder)
        os.makedirs(self.folder, exist_ok=True)

        self.selected_index = None  # 👈 به‌جای مسیر، عدد فایل انتخابی ذخیره می‌شود
        self.setWindowTitle("انتخاب یا ساخت فایل CSV")
        self.resize(480, 360)

        layout = QVBoxLayout(self)

        self.info_label = QLabel(f"پوشه: {self.folder}")
        layout.addWidget(self.info_label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.btn_new = QPushButton("ساخت فایل جدید")
        self.btn_select = QPushButton("انتخاب فایل")
        self.btn_cancel = QPushButton("انصراف")
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_select)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        # اتصال سیگنال‌ها
        self.btn_new.clicked.connect(self.create_new_file)
        self.btn_select.clicked.connect(self.select_file)
        self.btn_cancel.clicked.connect(self.reject)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.refresh_list()

        # اگر هیچ فایل CSV نبود، مستقیم دیالوگ ساخت فایل جدید را باز کن
        if self.list_widget.count() == 0:
            self.create_new_file()

    def refresh_list(self):
        """لیست فایل‌های CSV را از پوشه بخوان و با شماره نمایش بده"""
        self.list_widget.clear()
        self.csv_files = [f for f in os.listdir(self.folder) if f.lower().endswith(".csv")]
        self.csv_files.sort()
        for i, f in enumerate(self.csv_files, start=1):
            self.list_widget.addItem(f"{i}. {f}")

    def create_new_file(self):
        """از کاربر نام فایل می‌گیرد، فایل را می‌سازد و لیست را بروزرسانی می‌کند"""
        name, ok = QInputDialog.getText(self, "اسم فایل جدید", "نام فایل (بدون .csv):")
        if not ok:
            return
        name = name.strip()
        if not name:
            QMessageBox.warning(self, "خطا", "نام فایل نمی‌تواند خالی باشد.")
            return

        if not name.lower().endswith(".csv"):
            name = name + ".csv"

        path = os.path.join(self.folder, name)
        if os.path.exists(path):
            ret = QMessageBox.question(
                self, "فایل موجود است",
                f"فایل «{name}» از قبل وجود دارد. بازنویسی شود؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if ret != QMessageBox.StandardButton.Yes:
                return

        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Username", "peer_id"])

        QMessageBox.information(self, "ساخته شد", f"فایل ساخته شد:\n{path}")
        self.refresh_list()

    def select_file(self):
        """شماره فایل انتخاب‌شده را برمی‌گرداند"""
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "انتخاب", "ابتدا یک فایل را از لیست انتخاب کنید.")
            return

        text = item.text()
        self.selected_index = int(text.split(".")[0])  # 👈 فقط شماره را ذخیره کن
        self.accept()

    def on_item_double_clicked(self, item):
        """در صورت دوبار کلیک روی آیتم، همانند انتخاب عمل کن"""
        text = item.text()
        self.selected_index = int(text.split(".")[0])
        self.accept()


# --- مثال استفاده در برنامه اصلی ---
class ExampleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مثال انتخاب شماره فایل CSV")
        self.resize(500, 300)
        layout = QGridLayout(self)

        self.open_btn = QPushButton("باز کردن دیالوگ انتخاب CSV")
        self.result_label = QLabel("انتخاب‌شده: (هیچ شماره‌ای انتخاب نشده)")

        layout.addWidget(self.open_btn, 0, 0)
        layout.addWidget(self.result_label, 1, 0)

        self.open_btn.clicked.connect(self.open_csv_dialog)

    def open_csv_dialog(self):
        dlg = CSVChooserDialog(folder="../result_scraper", parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            selected_num = dlg.selected_index
            self.result_label.setText(f"{selected_num}")
        else:
            self.result_label.setText("انتخاب لغو شد.")


    def run(self):
        app = QApplication(sys.argv)
        w = ExampleWindow()
        w.show()
        sys.exit(app.exec())
