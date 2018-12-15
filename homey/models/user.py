class User:

    def __init__(self, _id, firstname, lastname, email, language,
                 roleIds):
        self._id = _id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.language = language
        self.roleIds = roleIds

    def __str__(self):
        return "[{self._id}] {self.firstname} {self.lastname}".format(self=self)
