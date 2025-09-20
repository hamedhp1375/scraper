import time

from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from logic.add_user_csv import Add_user_csv
from logic.add_user_to_target_grop import Add_user_to_target_grop
from logic.login import LoginCLI


class ScraperMain:
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

if __name__ == '__main__':
    profile_path = r"/profile"
    # start = ScraperMain(profile_path)
    # driver = start.driver
    # start_login = Login(driver)
    # start_login.login()
    # my_app=MyApp()
    # my_app.run()
    start_operate=False
    driver = None
    start_login = None
    while True:
        print("\n===== منو عملیات =====")
        print("1. اجرای Add_user_csv")
        print("2. اجرای Add_user_to_target_grop")
        print("3. خروج")

        choice = input("عدد عملیات مورد نظر را وارد کنید: ")
        if not start_operate:
            start_operate = True
            start = ScraperMain(profile_path)
            driver = start.driver
            start_login = LoginCLI(driver)
            start_login.login()
        if choice == "1":
            # driver = None

            start_add_user_csv = Add_user_csv(driver)
            fileName = start_add_user_csv.prepare_csv_file()
            start_add_user_csv.search()
            time.sleep(3)
            start_add_user_csv.add_user(fileName)
            start_login.login()
        elif choice == "2":
            target = Add_user_to_target_grop(driver)
            time.sleep(2)
            # target.read_file()
            # time.sleep(2)
            target.add_user_to_target_grop()
            start_login.login()
        elif choice == "3":
            print("خروج از برنامه...")
            break
        else:
            print("گزینه نامعتبر است. لطفا دوباره تلاش کنید.")


