import csv

from tamrin.users_list_peers import Users

class AddPeerUserToList:
    def __init__(self):
        peer_file = Users()
        peer_file.search_file()
        peer_file.creat_list_users()
        self.selected_file = peer_file.address_file()
        self.row=[]
    def read_list_users(self):

            with open(self.selected_file, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    print(row)  # چاپ هر ردیف
                    self.row.append(row)  # ذخیره در لیست

            return self.row
    def add_peer_user_to_list(self):
        pass
    def send_links(self):
        pass


x = AddPeerUserToList()
print("____________________")
x.read_list_users()
print("_______________________")