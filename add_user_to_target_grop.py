from scaraper_main import ScraperMain

class Target_grop(ScraperMain):
    def __init__(self, profile_path):
        input("Name csv file group")
        input("Link group eiata")

        super().__init__(profile_path)

    def get_user_id_list_csv(self):
        pass

    def add_user_to_target_group(self):
        pass