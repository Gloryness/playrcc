import os
import json

from base.utils.common import process_url_id

class Cache:
    def __init__(self):
        self.folder = os.path.abspath(f'{os.environ["USERPROFILE"]}/Documents/playrcc/')
        self.cache_folder = os.path.abspath(f'{os.environ["USERPROFILE"]}/Documents/playrcc/cache/')
        self.txt_folder = os.path.abspath(f'{os.environ["USERPROFILE"]}/Documents/playrcc/giveaways/')
        self.layout = '{}'

        if not os.path.exists(self.folder): # making sure all the folders exist to avoid errors
            os.makedirs(self.folder)
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)
        if not os.path.exists(self.txt_folder):
            os.makedirs(self.txt_folder)

    def cached(self, url):
        """
        :param url: Check if URL is cached or not
        :return: bool
        """
        url = process_url_id(url)
        return os.path.exists(f'{self.cache_folder}\\{url}.bin')
    
    def store(self, url, to_cache={}):
        """
        :param url: Name of the file
        :param to_cache: A dictionary that each key and value are going to be cached
        """
        cached = self.cached(url)
        filename = self.cache_folder + '\\' + process_url_id(url) + '.bin'
        if cached:
            with open(filename) as ff:
                try:
                    data = json.load(ff)
                except json.decoder.JSONDecodeError: # if the file is somehow 0 bytes
                    cached = False

        with open(filename, 'w') as f:
            if not cached:
                data = json.loads(self.layout)
            for cache in to_cache:
                data[cache] = to_cache.get(cache)
            json.dump(data, f, indent=3)

    def get(self, url):
        url = process_url_id(url)
        filename = self.cache_folder + '\\' + process_url_id(url) + '.bin'
        with open(filename) as ff:
            data = json.load(ff)
        return data

    def list_cache(self):
        return os.listdir(self.cache_folder)
