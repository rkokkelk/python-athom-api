from athom.common.net import AthomSession


class Manager:

    def __init__(self, homey=None, token=None, **kwargs):
        self.homey = homey
        self.token = token
        self.requiredScopes = []

        kwargs['base'] = f"{self.homey.url}/api/manager" + kwargs['base']

        # Set request.Session for API interaction
        self.s = AthomSession(token=self.token, **kwargs)

    def getScopes(self):
        return self.requiredScopes

    def verifyScopeRequired(self, scope):
        return scope in self.requiredScopes

    def _verify_id(self, value):
        if not value:
            raise ValueError("Expected id to be a string")
