class Homey:

    def __init__(self, _id, name, ipInternal, softwareVersion,
                 language, state, geolocation, users, role, token, apps, ipExternal=None):
        self._id = _id
        self.name = name
        self.ipInternal = ipInternal
        self.ipExternal = ipExternal
        self.softwareVersion = softwareVersion
        self.language = language
        self.state = state
        self.geolocation = geolocation
        self.users = users
        self.role = role
        self.token = token
        self.apps = apps

    def __str__(self):
        return "[{self._id}] {self.name} ({self.softwareVersion})".format(self=self)


    def authenticate(self):
        raise NotImplementedError()
