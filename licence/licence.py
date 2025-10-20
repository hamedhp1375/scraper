import requests


class Licence():
    def __init__(self, key):
        self.url = f"https://abtinafzar.ir/api/eitaa.php?license={key}"
        pass

    def check(self):
        try:
            r = requests.get(self.url, timeout=10)
            r.raise_for_status()
            try:
                dataclasses = r.json()

                if dataclasses.get("valid"):
                    return True

            except:
                pass
        except requests.exceptions.RequestException as e:
            print("Error request")

        return False
