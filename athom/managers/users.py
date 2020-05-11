import json
import logging

from athom.common import scopes
from athom.managers.manager import Manager

log = logging.getLogger(__name__)

class ManagerUsers(Manager):

    def __init__(self, **kwargs):
        super().__init__(base='/users', **kwargs)

        self.requiredScopes = []


    def login(self, delegationToken):
        data = {
            'token': delegationToken
        }

        r = self.s.post('/login', json=data).text.replace('"', '')
        self.token = r
        return r


    def getUsers(self):
        raise NotImplementedError()


    def createUser(self):
        raise NotImplementedError()


    def getUserMe(self):
        raise NotImplementedError()


    def updateUserMe(self):
        raise NotImplementedError()


    def deleteUserMe(self):
        raise NotImplementedError()


    def getUser(self):
        raise NotImplementedError()


    def updateUser(self):
        raise NotImplementedError()


    def deleteUser(self):
        raise NotImplementedError()


    def updateUserMeProperties(self):
        raise NotImplementedError()


    def deleteUserMeProperties(self):
        raise NotImplementedError()


    def getState(self):
        raise NotImplementedError()
