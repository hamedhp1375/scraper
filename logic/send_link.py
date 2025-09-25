import csv
import os

from logic.add_user_to_target_grop import Add_user_to_target_grop


class SendLink:
    def __init__(self, driver, file):
        self.driver = driver
        self.file = file
        self.peer_id_result = []

    def search_member(self):
        with open(self.file, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            if not reader:
                print("هیچ کاربری داخل فایل نیست")
                return

            for row in reader:
                self.peer_id_result.append(row["peer_id"])


    def send_link(self):
        pass
