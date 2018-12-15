class UserDevice:

    def __init__(self, _id, name, platform, token, appVersion,
                 created, updated, devMode, publicKey=""):
        self._id = _id
        self.name = name
        self.platform = platform
        self.token = token
        self.publicKey = publicKey
        self.appVersion = appVersion
        self.created = created
        self.updated = updated
        self.devMode = devMode

    def __str__(self):
        return "[{self._id}] {self.name} ({self.platform})".format(self=self)
