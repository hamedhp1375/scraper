import time

from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from add_user_csv import Add_user_csv
from login import Login


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
    profile_path = r"C:\pyton\eta_scraper\profile"
    start = ScraperMain(profile_path)
    driver = start.driver
    start_login = Login(driver)
    start_login.login()
    start_add_user_csv=Add_user_csv(driver)
    start_add_user_csv.serch()
    time.sleep(3)
    start_add_user_csv.add_user()
    time.sleep(3000)

























    #
    #
    # start_login.login()
    # time.sleep(2)
    # start_add_user = Add_user_csv(profile_path)
    # start_add_user.serch()
    # time.sleep(500)





    # while True:
    #
    #     input_ = input("Enter your purpose 1- get user from group save to csv \n 2- Add user from csv file to target group")
    #     if input_ == "1":
    #         assertss = AddUserCsv(profile_path)
    #         assertss.run()
    #         break
    #
    #     if input_ == "2":
    #
    #         pass