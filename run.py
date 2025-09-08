import time
from selenium.webdriver.common.action_chains import ActionChains

from add_user_csv import Add_user_csv
from login import Login
if __name__ == '__main__':
    profile_path = r"C:\pyton\eta_scraper\profile"
    start_login = Login(profile_path)
    start_login.login()
    time.sleep(2)
    start_add_user = Add_user_csv(profile_path)
    start_add_user.serch()
    time.sleep(500)





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