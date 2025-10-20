import time
from webbrowser import Elinks

from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
from PyQt6.QtWidgets import QApplication

from graphic.chose_data import FileSelector
from graphic.chose_graphic import MenuBox
from graphic.login_page import MainWindow
from graphic.number_user_add_grop import UserCountDialog
from graphic.send_cod import CodeWindow
from graphic.send_link import LinkInputWindow
from logic.add_user_csv import Add_user_csv, Add_user_csv_graphic
from logic.add_user_to_target_grop import Add_user_to_target_grop, Add_user_to_target_grop_graphic
from logic.login import LoginCLI, LoginGraphic
from logic.scaraper_main import ScraperMain
from logic.send_link import SendLink, Send_link_graphics

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()  # تا وقتی کاربر پنجره رو نبنده، اینجا منتظر می‌مونه

    # وقتی پنجره بسته شد:
    print("شماره واردشده:", window.phone_number)
    print("فایل انتخابی:", window.file_path)
    print(f"مقدار یوزرنیم {window.username}")
    print(f"{window.license}لایسنس برابر ")

    profile_path = r"/profile"
    numbers = window.phone_number
    username = window.username

    code = None
    start = ScraperMain(profile_path)
    driver = start.driver
    start_login = LoginGraphic(driver, numbers)
    if start_login.is_login_page():
        start_login.send_number()
        code_window = CodeWindow()
        code_window.exec()  # پنجره modal باز میشه و منتظر میمونه تا کاربر کد رو وارد کنه
        code = code_window.code
        start_login.send_code(code)

    # ✅ حلقه اصلی برنامه
    while True:
        menu_window = MenuBox()
        menu_window.exec()
        selected_option = menu_window.selection

        if selected_option == 1:
            # انتخاب فایل کاربران
            file_window = FileSelector()
            file_window.show()
            app.exec()
            file = int(file_window.selected_file_index)
            # وارد کردن لینک گروه
            send_link = LinkInputWindow()
            send_link.show()
            app.exec()
            link = send_link.link

            start_add_user_csv = Add_user_csv_graphic(driver, username, link)
            file_name = start_add_user_csv.prepare_csv_file(file)
            start_add_user_csv.search()
            time.sleep(3)
            start_add_user_csv.add_user(file_name)
            #
            time.sleep(3)
            start_login.return_home()

        elif selected_option == 2:
            send_link = LinkInputWindow()
            send_link.show()
            app.exec()
            link = send_link.link
            target_grop = Add_user_to_target_grop_graphic(driver, username, link)
            # انتخاب فایل کاربران
            file_window = FileSelector()
            file_window.show()
            app.exec()
            file = int(file_window.selected_file_index)
            start_add_user_csv = Add_user_csv_graphic(driver, username, link)
            file_name = start_add_user_csv.prepare_csv_file(file)
            cunt_user_dialog=UserCountDialog()
            cunt_user_dialog.show()
            app.exec()
            cunt_user=cunt_user_dialog.user_count
            time.sleep(1)
            target_grop.add_user_to_target_grop(file_name,cunt_user)
            start_login.return_home()

        elif selected_option == 3:
            file_window = FileSelector()
            file_window.show()
            app.exec()
            links = None
            file = int(file_window.selected_file_index)
            start_add_user_csv = Add_user_csv_graphic(driver, username, links)
            file_name = start_add_user_csv.prepare_csv_file(file)

            send_link_invrite = LinkInputWindow()
            send_link_invrite.show()
            app.exec()
            link = send_link_invrite.link
            invite_link = Send_link_graphics(driver, file_name, link)
            invite_link.search_member()
            invite_link.send_link()

        elif selected_option == 4:
            print("خروج از برنامه")
            driver.quit()
            break

        else:
            print("هیچ گزینه‌ای انتخاب نشد یا کاربر پنجره را بست.")

        print("\n✅ عملیات تمام شد. منو دوباره باز می‌شود...\n")
        time.sleep(2)

    time.sleep(1)
