import json

class AthomAPIConnectionError(Exception):
    """Error accesing API"""

class AthomTokenDBError(Exception):
    """Error getting Token from database"""

class AthomAPISessionError(Exception):
    """No valid OAUTH2 session required to access API's"""

    def __str__(self):
        return "No OAUTH2 session available for accessing API's"

class AthomAPIError(Exception):
    """General error while using API"""

    def __init__(self, error_content):
        error_dict = json.loads(error_content)

        if 'code' in error_dict:
            self.code = error_dict['code']
            self.error = error_dict['error']
            self.description = error_dict['error_description']

        else:
            self.code = error_dict['status']
            self.error = error_dict['result']
            self.description = 'Unknown error'

    def __str__(self):
        return f"[{self.code}] {self.error}: {self.description}"


class AthomCloudAuthenticationError(AthomAPIError):
    """Authentication error while accessing API"""

class AthomCloudGateWayAPIError(AthomAPIError):
    """API Gateway Error"""

    def __init__(self):
        self.code = 502
        self.error = 'Bad Gateway'
        self.description = 'Unknown bad gateway error'

class AthomCloudUnknownAPIError(AthomAPIError):
    """Unknown error from API"""
