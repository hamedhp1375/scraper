import os
import csv
import time

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from add_user_csv import Add_user_csv

usernames = []
class Add_user_to_target_grop:
    def __init__(self,driver):
        self.driver=driver
        search=Add_user_csv(driver)
        search.search()


    def read_file(self):
        # گرفتن همه فایل‌های csv موجود
        csv_files = [f for f in os.listdir() if f.endswith(".csv")]
        if not csv_files:
            print("❌ هیچ فایل CSV پیدا نشد.")
            return []

        print("\n📂 فایل‌های موجود:")
        for i, file in enumerate(csv_files, start=1):
            print(f"{i}. {file}")

        # انتخاب فایل
        while True:
            choice = input("شماره فایل مورد نظر را وارد کن: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(csv_files):
                selected_file = csv_files[int(choice) - 1]
                break
            print("❌ شماره نامعتبره، دوباره تلاش کن.")


        try:
            with open(selected_file, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)  # مستقیم با هدر کار می‌کنه
                for row in reader:
                    if row.get("Username"):  # فقط ستون Username
                        usernames.append(row["Username"].strip())
        except Exception as e:
            print("⚠️ خطا در خواندن فایل:", e)
            return []

        print(f"✅ {len(usernames)} نام کاربری از {selected_file} خونده شد.")
        return usernames

    def add_user_to_target_grop(self):
        get_title = self.driver.find_element(By.CSS_SELECTOR, "div.content > div.top > div.user-title > span.peer-title")
        self.driver.execute_script("arguments[0].click();", get_title)
        button_add=self.driver.find_element(By.CSS_SELECTOR, "button.btn-circle.btn-corner.z-depth-1.tgico-addmember_filled")
        self.driver.execute_script("arguments[0].click();", button_add)
        time.sleep(3)
        for username in usernames:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.selector-search > input.selector-search-input.i18n"))
            )
            search_input.send_keys(f"@{username}")
            time.sleep(3)

            first_checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.scrollable.scrollable-y > ul.chatlist > li.rp.chatlist-chat[data-peer-id]"))
            )
            self.driver.execute_script("arguments[0].click();", first_checkbox)
            print("✅ اولین کاربر انتخاب شد.")
            time.sleep(2)
        next_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btn-circle.btn-corner.z-depth-1.tgico-arrow_next.rp.is-visible"))
        )
        self.driver.execute_script("arguments[0].click();", next_button)
        print("✅ دکمه 'بعدی' کلیک شد.")
        time.sleep(2)
        add_button = self.driver.find_element(
            By.XPATH,
            "//div[contains(@class,'popup-buttons')]//button[span[text()='افزودن']]"
        )
        add_button.click()


