class User:

    def __init__(self, _id, firstname, lastname, email, language, roleIds,
                 avatar, devices, roles=list(), homeys=list()):
        self._id = _id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.language = language
        self.roles = roles
        self.roleIds = roleIds
        self.avatar = avatar
        self.homeys = homeys
        self.devices = devices

    def __str__(self):
        return "[{self._id}] {self.firstname} {self.lastname}".format(self=self)


    def getDevice(self, d_id):

        for device in self.devices:
            if device._id == d_id:
                return device

        raise LookupError()


    def getHomeys(self):
        return self.homeys


    def getHomeyById(self, h_id):

        for homey in self.homeys:
            if homey._id == h_id:
                return homey

        raise LookupError()


    def getFirstHomey(self):

        if self.homeys:
            return self.homeys[0]

        raise LookupError()
