class Manager:

    def __init__(self, homey=None, token=None):
        self.homey = homey
        self.token = token
        self.requiredScopes = []


    def getScopes(self):
        return self.requiredScopes


    def verifyScopeRequired(self, scope):
        return scope in self.requiredScopes


    def _verify_id(self, value):
        if not value:
            raise ValueError("Expected id to be a string")
