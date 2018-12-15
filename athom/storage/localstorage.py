import json
import logging

log = logging.getLogger(__name__)

class LocalStorage:

    def __init__(self, path="homeyLocalStorage.db"):

        self.path = path
        self.storage = dict()

        with open(self.path, 'r') as f:
            self.storage = json.load(f)


    def set(self, key, value):
        self.storage[key] = value

        with open(self.path, 'w') as f:
            json.dump(self.storage, f)


    def get(self, key):

        with open(self.path, 'r') as f:
            self.storage = json.load(f)

        return self.storage[key]


    def __contains__(self, m):
        return self.storage is not None and m in self.storage
