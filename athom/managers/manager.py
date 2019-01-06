class Manager:

    def __init__(self, homey=None, token=None):
        self.homey = homey
        self.token = token
        self.requiredScopes = []


    def getScopes(self):
        return self.requiredScopes


    def verifyScopeRequired(self, scope):
        return scope in self.requiredScopes
