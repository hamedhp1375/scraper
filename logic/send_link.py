import csv
import os
import time


from selenium.webdriver.common.by import By

from logic.add_user_to_target_grop import Add_user_to_target_grop


class SendLink:
    def __init__(self, driver, file):
        self.input_link=input("لینک دعوت را وارد کنید: ")
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
        for item in self.peer_id_result:
            self.driver.get(f"https://web.eitaa.com/#{item}")
            time.sleep(1)
            input_link = self.driver.find_element(By.CSS_SELECTOR,
                                                  "div.input-message-input.scrollable.scrollable-y.i18n.no-scrollbar")
            input_link.send_keys(f"{self.input_link}")
            time.sleep(1)
            send = self.driver.find_element(By.CSS_SELECTOR, "button.btn-icon.tgico-none.btn-circle")
            send.click()
            time.sleep(1)
            self.driver.get(f"https://web.eitaa.com")
            time.sleep(1)
            print(f"ارسال به {item}")


class Send_link_graphics:
    def __init__(self, driver, file,link):
        self.driver = driver
        self.file = file
        self.link = link
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
        for item in self.peer_id_result:
            self.driver.get(f"https://web.eitaa.com/#{item}")
            time.sleep(1)
            input_link = self.driver.find_element(By.CSS_SELECTOR,
                                                  "div.input-message-input.scrollable.scrollable-y.i18n.no-scrollbar")
            input_link.send_keys(f"{self.link}")
            time.sleep(1)
            send = self.driver.find_element(By.CSS_SELECTOR, "button.btn-icon.tgico-none.btn-circle")
            send.click()
            time.sleep(1)
            self.driver.get(f"https://web.eitaa.com")
            time.sleep(1)
            print(f"ارسال به {item}")