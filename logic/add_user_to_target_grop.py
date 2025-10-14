import os
import csv
import re
import time

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from logic.add_user_csv import Add_user_csv, Add_user_csv_graphic

usernames = []


class Add_user_to_target_grop:
    def __init__(self, driver):
        self.driver = driver
        search = Add_user_csv(driver)
        search.search()

    def read_file(self, file_result="../result_scraper"):
        # گرفتن همه فایل‌های csv موجود
        csv_files = [f for f in os.listdir(file_result) if f.endswith(".csv")]
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

        users = []
        try:
            selected_path = os.path.join(file_result, selected_file)
            with open(selected_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    username = row.get("Username", "").strip()

                    # پاکسازی شماره: حذف فاصله و کاراکترهای غیرعددی به جز +
                    raw_phone = row.get("Phone", "").strip()
                    phone = re.sub(r"[^\d+]", "", raw_phone)

                    users.append((username, phone))
        except Exception as e:
            print("⚠️ خطا در خواندن فایل:", e)
            return []

        print(f"✅ {len(users)} ردیف از {selected_file} خونده شد.")
        return users

    def add_user_to_target_grop(self):
        get_title = self.driver.find_element(By.CSS_SELECTOR,
                                             "div.content > div.top > div.user-title > span.peer-title")
        self.driver.execute_script("arguments[0].click();", get_title)
        button_add = self.driver.find_element(By.CSS_SELECTOR,
                                              "button.btn-circle.btn-corner.z-depth-1.tgico-addmember_filled")
        self.driver.execute_script("arguments[0].click();", button_add)
        time.sleep(3)

        users = self.read_file()  # لیست تاپل‌ها

        for username, phone in users:
            search_value = None

            if username:  # اگر username موجوده
                # بررسی اینکه username فقط عدد یا + هست و فاصله‌ها رو حذف کن
                if re.fullmatch(r"\+?\d+(?:\s?\d+)*", username):
                    search_value = username.replace(" ", "")
                else:
                    search_value = f"@{username}"  # رشته واقعی، @ اضافه کن
            elif phone:  # اگر username خالیه و شماره موجوده
                search_value = phone.replace(" ", "")  # شماره، بدون @ و فاصله

            if not search_value:
                continue  # هیچ چیزی برای سرچ نیست

            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.selector-search > input.selector-search-input.i18n"))
            )
            search_input.clear()
            search_input.send_keys(search_value)
            time.sleep(3)

            first_checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.scrollable.scrollable-y > ul.chatlist > li.rp.chatlist-chat[data-peer-id]"))
            )
            self.driver.execute_script("arguments[0].click();", first_checkbox)
            print(f"✅ اولین کاربر انتخاب شد: {search_value}")
            time.sleep(2)

        # کلیک روی دکمه بعدی و افزودن
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


class Add_user_to_target_grop_graphic:
    def __init__(self, driver, username, link):
        self.driver = driver
        self.username = username
        self.link = link
        search = Add_user_csv_graphic(driver, username, link)
        search.search()

    def read_file_garphic(self, file):
        selected_file = file
        users = []
        try:
            selected_path = os.path.join(selected_file)
            with open(selected_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    username = row.get("Username", "").strip()

                    # پاکسازی شماره: حذف فاصله و کاراکترهای غیرعددی به جز +
                    raw_phone = row.get("Phone", "").strip()
                    phone = re.sub(r"[^\d+]", "", raw_phone)

                    users.append((username, phone))

        except Exception as e:
            print("⚠️ خطا در خواندن فایل:", e)
            return []

        print(f"✅ {len(users)} ردیف از {selected_file} خونده شد.")
        return users

    def add_user_to_target_grop(self, file):
        get_title = self.driver.find_element(By.CSS_SELECTOR,
                                             "div.content > div.top > div.user-title > span.peer-title")
        self.driver.execute_script("arguments[0].click();", get_title)
        button_add = self.driver.find_element(By.CSS_SELECTOR,
                                              "button.btn-circle.btn-corner.z-depth-1.tgico-addmember_filled")
        self.driver.execute_script("arguments[0].click();", button_add)
        time.sleep(3)

        users = self.read_file_garphic(file)  # لیست تاپل‌ها

        count = 0  # ✅ شمارنده اضافه شد

        for username, phone in users:
            if count >= 200:  # ✅ اگر تعداد به 200 رسید، متوقف شو
                print("⛔️ به 200 نفر رسیدیم، عملیات متوقف شد.")
                break

            search_value = None

            if username:  # اگر username موجوده
                if re.fullmatch(r"\+?\d+(?:\s?\d+)*", username):
                    search_value = username.replace(" ", "")
                else:
                    search_value = f"@{username}"
            elif phone:
                search_value = phone.replace(" ", "")

            if not search_value:
                continue

            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.selector-search > input.selector-search-input.i18n"))
            )
            search_input.clear()
            search_input.send_keys(search_value)
            time.sleep(3)

            first_checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.scrollable.scrollable-y > ul.chatlist > li.rp.chatlist-chat[data-peer-id]"))
            )
            self.driver.execute_script("arguments[0].click();", first_checkbox)
            print(f"✅ کاربر شماره {count + 1}: {search_value}")
            count += 1  # ✅ بعد از هر افزودن، شمارنده زیاد می‌شود
            time.sleep(2)

        # کلیک روی دکمه بعدی و افزودن
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
