import csv
import os
import time
from result_scraper import *

from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Add_user_csv:
    def __init__(self, driver):
        self.driver = driver


    def search(self):
        save_msg=input("نام کاربری را وارد کنید:")
        self.driver.get(f"https://web.eitaa.com/#@{save_msg}")
        # save_msg_li = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((
        #         By.XPATH,
        #         "//li[contains(@class,'chatlist-chat')]//span[@class='i18n' and text()='پیام های ذخیره شده']/ancestor::li"
        #     ))
        # )
        #
        # save_msg_li.click()

        # self.driver.get("https://web.eitaa.com/#26136928")
        try:
            saved_item = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.chatlist-chat[data-peer-id='26136928']"))
            )
            self.driver.execute_script("arguments[0].click();", saved_item)
            print("✅ روی پیام‌های ذخیره شده کلیک شد.")
        except (TimeoutException, StaleElementReferenceException) as e:
            print("⚠️ خطا در کلیک روی 'پیام های ذخیره شده':", e)
            return

        try:
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.input-message-input[contenteditable='true']"))
            )
            link_member_grup = input("لطفا لینک را وارد کنید: ")
            input_box.send_keys(link_member_grup)
            print("✅ لینک وارد شد.")
        except Exception as e:
            print("⚠️ خطا در وارد کردن لینک:", e)
            return

        try:
            send_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-send"))
            )
            self.driver.execute_script("arguments[0].click();", send_button)
            print("✅ پیام ارسال شد.")
        except Exception as e:
            print("⚠️ خطا در ارسال پیام:", e)
            return

        try:
            # صبر تا لینک‌ها لود شوند و گرفتن آخرین لینک
            links = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.bubble a.anchor-url"))
            )
            if not links:
                print("⚠️ لینکی پیدا نشد.")
                return
            last_link = links[-1]
            self.driver.execute_script("arguments[0].click();", last_link)
            print("✅ روی آخرین لینک کلیک شد.")
        except (TimeoutException, StaleElementReferenceException) as e:
            print("⚠️ خطا در کلیک روی آخرین لینک:", e)
            return


    def add_user(self,filename):
        filename = filename
        try:
            # کلیک روی المان نمایش تعداد اعضا (صبر تا قابل کلیک شدن)
            members_elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.chat-info div.person div.content div.bottom div.info span.i18n"))
            )
            self.driver.execute_script("arguments[0].click();", members_elem)
            print("✅ روی تعداد اعضا کلیک شد.")

            # صبر تا لیست اعضای جستجو ظاهر شود
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-super-content-members"))
            )

            # گرفتن همه اعضا (li)
            members = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.search-super-content-members > ul.chatlist > li.chatlist-chat"
            )

            peer_ids = []
            for el in members:
                pid = el.get_attribute("data-peer-id")
                if not pid:
                    continue
                # اگر مالک هست ردش کن
                try:
                    el.find_element(By.XPATH, ".//span[contains(text(), 'مالک')]")
                    continue
                except:
                    pass
                peer_ids.append(pid)

            print(f"🔢 تعداد اعضای قابل بررسی: {len(peer_ids)}")

            # خواندن نام‌های موجود از فایل CSV (تشخیص ستون Username از هدر)
            existing_usernames = set()
            if os.path.exists(filename):
                try:
                    with open(filename, "r", encoding="utf-8") as csvfile:
                        reader = csv.reader(csvfile)
                        header = next(reader, None)
                        if header:
                            # پیدا کردن شاخص ستون Username اگر وجود داشت
                            if "Username" in header:
                                uname_idx = header.index("Username")
                            elif len(header) >= 2:
                                # اگر فرمت ID,Username,Phone بود، ستون Username معمولاً 1 است
                                uname_idx = 1
                            else:
                                uname_idx = 0
                        else:
                            uname_idx = 0

                        for row in reader:
                            if row and len(row) > uname_idx:
                                existing_usernames.add(row[uname_idx].strip())
                except Exception as e:
                    print("⚠️ خطا در خواندن فایل CSV موجود:", e)

            new_users = []  # لیست تاپل (username, phone)

            for peer_id in peer_ids:
                try:
                    # پیدا کردن عضو براساس peer_id (صبر تا حضور)
                    member_li = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, f"div.search-super-content-members > ul.chatlist > li.chatlist-chat[data-peer-id='{peer_id}']")
                        )
                    )
                    # کلیک ایمن روی عضو
                    self.driver.execute_script("arguments[0].click();", member_li)
                    print(f"✅ روی عضو با peer_id {peer_id} کلیک شد.")
                    # صبر تا بخش پروفایل کاربر لود شود
                    WebDriverWait(self.driver, 7).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.sidebar-left-section-content"))
                    )
                    time.sleep(0.5)

                    # گرفتن username (اگر وجود داشت)
                    username = ""
                    try:
                        username_elem = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.row-title.tgico-username"))
                        )
                        username = username_elem.text.strip()
                    except:
                        username = ""

                    # گرفتن phone (اگر وجود داشت)
                    phone = ""
                    try:
                        phone_elem = self.driver.find_element(By.CSS_SELECTOR, "div.row-title.tgico-phone")
                        phone = phone_elem.text.strip()
                    except:
                        phone = ""

                    # اگر هم username و هم phone خالی بود، نادیده بگیر
                    # اگر هم username و هم phone خالی بود، نادیده بگیر
                    if not username and not phone:
                        print(f"⚠️ برای peer_id {peer_id} هیچ نام کاربری یا تلفنی پیدا نشد.")
                    else:
                        if username:  # اگر یوزرنیم موجود بود
                            if username not in existing_usernames:
                                new_users.append((username, phone))
                                existing_usernames.add(username)
                                print(f"➕ جدید (با یوزرنیم): {username} | {phone}")
                        elif phone:  # اگر یوزرنیم نداشت ولی شماره داشت
                            if phone not in existing_usernames:
                                new_users.append((phone, phone))
                                existing_usernames.add(phone)
                                print(f"➕ جدید (فقط شماره): {phone}")

                    # برگشت به لیست اعضا و صبر تا لود شدن
                    time.sleep(0.5)
                    self.driver.back()
                    time.sleep(0.5)
                    WebDriverWait(self.driver, 7).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-super-content-members"))
                    )


                except Exception as e:
                    print(f"⚠️ خطا در پردازش peer_id={peer_id}: {e}")
                    # سعی می‌کنیم به لیست اعضا برگردیم تا حلقه ادامه پیدا کند
                    try:
                        self.driver.back()
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-super-content-members"))
                        )
                        time.sleep(0.5)
                    except:
                        pass
                    continue

            # نوشتن نام‌های جدید در فایل CSV با ID ترتیبی و ستون Phone
            if new_users:
                file_exists = os.path.exists(filename)
                with open(filename, "a", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(["ID", "Username", "Phone"])

                    # محاسبه ID شروعی (بر اساس تعداد ردیف‌های قبلی)
                    start_id = 1
                    if file_exists:
                        try:
                            with open(filename, "r", encoding="utf-8") as f:
                                existing_lines = sum(1 for _ in f) - 1  # کم کردن هدر
                                start_id = existing_lines + 1
                        except:
                            start_id = 1

                    for idx, (username, phone) in enumerate(new_users, start=start_id):
                        writer.writerow([idx, username, phone if phone else ""])
                print("نام‌های کاربری جدید در فایل ذخیره شد.")
            else:
                print("نام جدیدی برای ذخیره وجود نداشت.")

        except Exception as e:
            print("⚠️ خطای کلی در add_user:", e)

    def prepare_csv_file(self, folder="../result_scraper"):
        """
        ساخت فایل جدید یا انتخاب فایل موجود و برگرداندن نام فایل CSV
        """

        # اگه پوشه وجود نداشت، بساز
        if not os.path.exists(folder):
            os.makedirs(folder)

        create_new = input("میخوای فایل جدید بسازی؟ (y/n): ").strip().lower()
        if create_new == 'y':
            new_name = input("اسم فایل جدید را وارد کن (بدون .csv): ").strip()
            if not new_name.endswith(".csv"):
                new_name += ".csv"

            # مسیر کامل فایل
            file_path = os.path.join(folder, new_name)

            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Username", "Phone"])
            print(f"✅ فایل {file_path} ساخته شد.")

        # گرفتن همه فایل‌های CSV موجود در پوشه
        csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]
        if not csv_files:
            print("⚠️ هیچ فایل CSV موجود نیست. لطفا فایل جدید بساز.")
            return self.prepare_csv_file(folder)

        print("\n📂 فایل‌های موجود:")
        for i, file in enumerate(csv_files, start=1):
            print(f"{i}. {file}")

        while True:
            choice = input("شماره فایل مورد نظر را وارد کن: ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(csv_files):
                    # مسیر کامل فایل انتخاب‌شده
                    selected_file = os.path.join(folder, csv_files[choice - 1])
                    print(f"✅ فایل انتخاب شد: {selected_file}")
                    return selected_file
            print("❌ شماره نامعتبر است. دوباره تلاش کن.")
