import json

class AthomAPIError(Exception):
    """General error while using API"""

    def __init__(self, error_content):
        error_dict = json.loads(error_content)

        self.code = error_dict['code']
        self.error = error_dict['error']
        self.description = error_dict['error_description']

    def __str__(self):
        return "[{self.code}] {self.error}: {self.description}".format(self=self)


class AthomCloudAuthenticationError(AthomAPIError):
    """Authentication error while accessing API"""

class AthomCloudUnknownAPIError(AthomAPIError):
    """Unknown error from API"""
