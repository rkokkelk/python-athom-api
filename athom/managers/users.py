import json
import logging

from athom.common import scopes
from athom.common.net import delete, get, post
from athom.managers.manager import Manager

log = logging.getLogger(__name__)

class ManagerUsers(Manager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.homeyPath = "{homey.url}/api/manager/users".format(homey=self.homey)
        self.requiredScopes = []


    def login(self, delegationToken):
        url = self.homeyPath + '/login'

        data = {
            'token': delegationToken
        }

        r = post(url, json=data).replace('"', '')
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
