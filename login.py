import time

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

from scaraper_main import ScraperMain


class Login:
    def __init__(self, drive):
        self.driver = drive

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

