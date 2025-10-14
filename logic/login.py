import time

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait


class Login:
    def __init__(self, drive):
        self.driver = drive

    def login(self):
        pass

    def check_I_am_in_phone_input(self):
        pass

    def check_code_input(self):
        pass


class LoginCLI(Login):
    def __init__(self, drive):
        super().__init__(drive)

    def login(self):
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
        except Exception as e:
            print("❌ Error: ", e)
        pass


class LoginGraphic(Login):
    def __init__(self, drive, number):
        super().__init__(drive)
        self.number = number
        self.is_login = False

    def is_login_page(self):
        self.driver.get("https://web.eitaa.com/")
        time.sleep(5)  # صبر برای لود اولیه
        """برمی‌گردونه True اگر صفحه لاگین بازه"""
        login_inputs = self.driver.find_elements(By.CSS_SELECTOR, "div.input-field-input[inputmode='decimal']")
        if login_inputs:
            print("📲 وارد صفحه لاگین شدیم")
            return True
        else:
            print("✅ قبلاً لاگین شده یا صفحه لاگین نیست")
            return False

    #     چون نمبشه هر دو تا با هم اورد باید اول شماره وارد بشه بعد کد پس باید تابع لاگین به دو بخش تبدیل کرد
    def send_number(self):
        """شماره رو وارد می‌کنه و دکمه ادامه رو می‌زنه"""
        login_inputs = self.driver.find_elements(By.CSS_SELECTOR, "div.input-field-input[inputmode='decimal']")
        if not login_inputs:
            print("صفحه لاگین پیدا نشد")
            return

        fon_div = login_inputs[0]
        fon_div_button_inter = self.driver.find_element(
            By.CSS_SELECTOR, "button.btn-primary.btn-color-primary.rp"
        )

        fon_div.click()
        fon_div.send_keys(self.number)
        print(f"شماره وارد شد: {self.number}")
        fon_div_button_inter.click()

    def send_code(self, cod):
        """کد دریافتی رو وارد می‌کنه"""
        try:
            code_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.input-field-input[type='tel']"))
            )
            code_input.click()
            code_input.send_keys(cod)
            print(f"کد وارد شد: {cod}")
            print("✅ لاگین کامل شد.")
        except Exception as e:
            print("❌ خطا در وارد کردن کد:", e)

    def login(self, cod):
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
                inter_number = self.number
                fon_div.send_keys(inter_number)
                print(f"input number= {inter_number}")
                fon_div_button_inter.click()

                # صبر می‌کنیم تا input کد باز بشه
                code_input = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input.input-field-input[type='tel']"))
                )
                code_input.click()
                inter_code = cod
                code_input.send_keys(inter_code)

                print("✅ لاگین انجام شد.")
            else:
                print("✅ قبلاً لاگین شده‌ای، نیازی به ورود دوباره نیست.")
                print(f"input number= {self.number}")
        except Exception as e:
            print("❌ Error: ", e)
        pass
    def return_home(self):
        self.driver.get("https://web.eitaa.com/")