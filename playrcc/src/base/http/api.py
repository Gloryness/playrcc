import requests
from bs4 import BeautifulSoup

class API:
    def __init__(self, auth):
        self.auth = auth
        self.api = 'https://api.playr.gg/api/enter'
        self.headers = {
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "en-GB, en;q=0.5",
            'Authorization': self.auth, # an authentication is needed other we cannot use it and a response will say 'Missing JWT Token'
            'Host': "api.playr.gg",
            'Origin': 'https://playr.gg',
            'sec-fetch-dest': "empty",
            'sec-fetch-mode': "cors",
            'sec-fetch-site': "same-site",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
        }
        self.params = {
            "dry_run": False,
            "entry_method": "playr_secret_code"
        }


    def send_post(self, params={}):
        """
        Send a POST request to the API
        :return: text
        """
        self.params.update(params)

        r = requests.post(self.api, params=self.params, headers=self.headers) # sending the post request

        self.params = { # resetting the params
            "dry_run": False,
            "entry_method": "playr_secret_code"
        }

        return r.text # returning the response

    @staticmethod
    def get_auth():
        try:
            r = requests.get('https://pastebin.com/UMWjEWdg').text
        except:
            return 'None'
        soup = BeautifulSoup(r, 'lxml')
        return soup.find(class_='de1').text