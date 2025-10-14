import tkinter as tk
from tkinter import filedialog

class DialogBox:
    def __init__(self):
        # ایجاد پنجره اصلی و مخفی کردنش
        self.root = tk.Tk()
        self.root.withdraw()
        self.file_path = None

    def select_file(self):
        """باز کردن دیالوگ انتخاب پوشه و برگرداندن مسیر آن"""
        self.file_path = filedialog.askdirectory(
            title="یک پوشه انتخاب کنید"
        )

        if self.file_path:
            return self.file_path
        else:
            print("پوشه‌ای انتخاب نشد.")
            return None


# ✅ استفاده از کلاس:
if __name__ == "__main__":
    dialog = DialogBox()
    path = dialog.select_file()
    print("نتیجه بازگشتی:", path)
