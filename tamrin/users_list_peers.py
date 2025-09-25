import csv
import os
from re import search


file = "../peer_id_result"
class Users:
    def __init__(self):
        self.file=file
        self.nofile=False
        self.new_file = input("ایا میخواهید فایل جدید بسازید y/n")
        self.selected_file=None


    def search_file(self):

        if self.new_file == "n":
            csv_files = [f for f in os.listdir(self.file) if f.endswith(".csv")]
            if not csv_files:
                self.nofile = True
                print("فایلی برای ارسال لینک وجود ندارد")
                return self.nofile
            for i, file in enumerate(csv_files, start=1):
                print(f"{i}. {file}")

            while True:
                choice = input("شماره فایل مورد نظر را وارد کن: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(csv_files):
                    self.selected_file = csv_files[int(choice) - 1]
                    print(self.selected_file)
                    return self.selected_file
                    break
                print("❌ شماره نامعتبره، دوباره تلاش کن.")

    def creat_list_users(self):

        if self.nofile or self.new_file == "y":
            new_name = input("اسم فایل جدید را وارد کن (بدون .csv): ").strip()
            if not new_name.endswith(".csv"):
                new_name += ".csv"

            # مسیر کامل فایل
            file_path = os.path.join(self.file, new_name)

            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "peer_id"])
            print(f"✅ فایل {file_path} ساخته شد.")
            self.selected_file = new_name
            return self.selected_file

    def address_file(self):
        file = self.file + "/" + self.selected_file
        return file


# q=Users()
# a=q.search_file()
# q.creat_list_users()
# print(q.read_list_users())
