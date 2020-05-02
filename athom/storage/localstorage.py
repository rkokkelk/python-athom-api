import os
import json
import logging

from athom.common.exceptions import AthomTokenDBError

from json.decoder import JSONDecodeError

log = logging.getLogger(__name__)

class LocalStorage:

    def __init__(self, path="homeyLocalStorage.db"):

        self.path = path

        try:
            self.storage = self.__parsedb__()
        except AthomTokenDBError:
            self.storage = dict()


    def set(self, key, value):
        self.storage[key] = value

        with open(self.path, 'w') as f:
            json.dump(self.storage, f)


    def get(self, key):
        self.storage = self.__parsedb__()
        return self.storage[key]


    def __contains__(self, m):
        return self.storage is not None and m in self.storage


    def __parsedb__(self):

        try:
            with open(self.path, 'r') as f:
                return json.load(f)

        except (FileNotFoundError, JSONDecodeError) as e:
            message = f"Failed to retrieve token from: {self.path}"

            log.error(message)
            raise AthomTokenDBError(message)
