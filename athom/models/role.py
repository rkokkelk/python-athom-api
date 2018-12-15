class Role:

    def __init__(self, _id, name, scopes):
        self._id = _id
        self.name = name
        self.scopes = scopes

    def __str__(self):
        return "[{self._id}] {self.name}".format(self=self)
