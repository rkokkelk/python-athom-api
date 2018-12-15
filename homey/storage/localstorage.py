import json
import logging

log = logging.getLogger(__name__)

class LocalStorage:

    path = None
    storage = dict()


    def __init__(self, path="homeyLocalStorage.db"):

        self.path = path

        with open(self.path, 'r') as f:
            self.storage = json.load(f)


    def set(self, key, value):
        self.storage[key] = value

        with open(self.path, 'w') as f:
            json.dump(value, f)


    def get(self, key):

        with open(self.path, 'r') as f:
            self.storage = json.load(f)

        return self.storage[key]


    def __contains__(self, m):
        log.debug("Verifying %s in storage", m)
        return self.storage is not None and m in self.storage
