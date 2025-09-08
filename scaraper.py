import csv
import os
import time
from encodings.punycode import selective_find

from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from trio import sleep_forever

member_per_id = []


class Eta_scaraper:
    def __init__(self, profile_path):
        self.profile_path = profile_path
        self.driver = self.init_driver()

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.5938.132 Safari/537.36"
        )
        return webdriver.Chrome(options=chrome_options)

    def run(self):
        try:
            self.driver.get("https://web.eitaa.com/")
            time.sleep(5)  # صبر برای لود اولیه

            # چک می‌کنیم input شماره وجود داره یا نه
            login_inputs = self.driver.find_elements(By.CSS_SELECTOR, "div.input-field-input[inputmode='decimal']")

            if login_inputs:  # یعنی صفحه لاگین بازه
                print("📲 وارد مرحله لاگین شدیم...")

                fon_div = login_inputs[0]
                fon_div_button_inter = self.driver.find_element(
                    By.CSS_SELECTOR, "button.btn-primary.btn-color-primary.rp"
                )

                fon_div.click()
                inter_number = input("شماره خود را وارد کنید  = ")
                fon_div.send_keys(inter_number)
                fon_div_button_inter.click()

                # صبر می‌کنیم تا input کد باز بشه
                code_input = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input.input-field-input[type='tel']"))
                )
                code_input.click()
                inter_code = input("کد را وارد کنید = ")
                code_input.send_keys(inter_code)

                print("✅ لاگین انجام شد.")
            else:
                print("✅ قبلاً لاگین شده‌ای، نیازی به ورود دوباره نیست.")

            # سرچ گروه
            self.serch()
            time.sleep(10)
            # # اد کردن اعضا
            self.add_user()
            # گروه هدف
            # self.get_id()
            self.target_grop()

            time.sleep(30000)

        except Exception as e:
            print("❌ Error: ", e)
            self.driver.quit()
            self.driver = self.init_driver()


    def serch(self):
        self.driver.get("https://web.eitaa.com/#26136928")
        time.sleep(5)  # صبر برای لود کامل صفحه

        # 2️⃣ کلیک روی "پیام‌های ذخیره شده"
        try:
            saved_item = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.chatlist-chat[data-peer-id='26136928']"))
            )
            saved_item.click()
            print("✅ روی پیام‌های ذخیره شده کلیک شد.")
        except (TimeoutException, StaleElementReferenceException) as e:
            print("⚠️ خطا در کلیک روی 'پیام های ذخیره شده':", e)

        # 3️⃣ پیدا کردن input و وارد کردن لینک
        try:
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.input-message-input[contenteditable='true']"))
            )
            link_member_grup = input("لطفا لینک را وارد کنید: ")
            input_box.send_keys(link_member_grup)
            print("✅ لینک وارد شد.")
        except Exception as e:
            print("⚠️ خطا در وارد کردن لینک:", e)

        # 4️⃣ کلیک روی دکمه ارسال
        try:
            send_button = self.driver.find_element(By.CSS_SELECTOR,
                                                   "button.btn-send")
            send_button.click()
            print("✅ پیام ارسال شد.")
        except Exception as e:
            print("⚠️ خطا در ارسال پیام:", e)

        try:
            # صبر تا آخرین پیام لود شود
            last_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.bubble a.anchor-url"))
            )[-1]  # گرفتن آخرین لینک

            # کلیک روی آخرین لینک
            self.driver.execute_script("arguments[0].click();", last_link)
            print("✅ روی آخرین لینک کلیک شد.")
        except (TimeoutException, StaleElementReferenceException) as e:
            print("⚠️ خطا در کلیک روی آخرین لینک:", e)


    def add_user(self):
        try:
            # پیدا کردن span که تعداد اعضا را نشان می‌دهد
            members_elem = self.driver.find_element(
                By.CSS_SELECTOR,
                "div.chat-info div.person div.content div.bottom div.info span.i18n"
            )

            # کلیک روی المان
            self.driver.execute_script("arguments[0].click();", members_elem)
            print("✅ روی تعداد اعضا کلیک شد.")

            members = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.search-super-content-members > ul.chatlist > li.chatlist-chat"
            )

            peer_ids = []
            for el in members:
                try:
                    el.find_element(By.XPATH, ".//span[contains(text(), 'مالک')]")
                    continue  # مالک → رد می‌کنیم
                except:
                    pass
                peer_ids.append(el.get_attribute("data-peer-id"))

            # خواندن نام‌های موجود از فایل CSV
            filename = "usernames.csv"
            existing_usernames = set()
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader, None)  # رد کردن هدر
                    for row in reader:
                        if row:
                            existing_usernames.add(row[0])

            # ذخیره نام‌های جدید
            new_usernames = []

            for peer_id in peer_ids:
                try:
                    # پیدا کردن li بر اساس data-peer-id
                    member_li = self.driver.find_element(
                        By.CSS_SELECTOR,
                        f"div.search-super-content-members > ul.chatlist > li.chatlist-chat[data-peer-id='{peer_id}']"
                    )

                    # کلیک روی عضو
                    member_li.click()
                    print(f"✅ روی عضو با peer_id {peer_id} کلیک شد.")
                    time.sleep(3)

                    username_div = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "div.row.row-with-icon.row-with-padding.row-clickable.hover-effect.rp div.row-title.tgico-username"
                    )
                    username = username_div.text

                    # اگر نام کاربری جدید بود، اضافه کن
                    if username not in existing_usernames:
                        new_usernames.append(username)
                        existing_usernames.add(username)
                        print(f"نام کاربری ذخیره شد: {username}")

                    # بازگشت عقب
                    self.driver.back()
                    time.sleep(2)

                except Exception as e:
                    print(f"⚠️ خطا در کلیک روی عضو با peer_id {peer_id}:", e)

            # نوشتن نام‌های جدید در فایل CSV
            if new_usernames:
                file_exists = os.path.exists(filename)
                with open(filename, "a", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(["Username"])  # هدر ستون
                    for username in new_usernames:
                        writer.writerow([username])

                print("نام‌های کاربری جدید در فایل usernames.csv ذخیره شد.")
            else:
                print("نام جدیدی برای ذخیره وجود نداشت.")

        except Exception as e:
            print("⚠️ خطا در کلیک روی تعداد اعضا:", e)

    def get_id(self):
        self.serch()
        time.sleep(10)
        usernames = []
        try:
            with open("usernames.csv", "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # رد کردن هدر
                for row in reader:
                    if row:  # اگر سطر خالی نبود
                        usernames.append(row[0])
        except FileNotFoundError:
            print("⚠️ فایل usernames.csv پیدا نشد.")

        return usernames

    def target_grop(self):
        ids = self.get_id()
        



if __name__ == "__main__":
    profile_path = r"C:\path\to\custom\profile"
    iranmodares = Eta_scaraper(profile_path)
    iranmodares.run()
