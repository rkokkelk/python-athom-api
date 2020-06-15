import logging

from athom.managers.manager import Manager
from athom.models.managers.users import UserSchema

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
        r = self.s.get('/user')
        schema = UserSchema(many=True)
        return schema.load(r.json().values())

    def createUser(self, **kwargs):
        json = UserSchema.dump(kwargs.get('user'))
        return self.s.post('/user', json=json)

    def getUserMe(self):
        r = self.s.get('/user/me')
        return UserSchema().load(r.json())

    def updateUserMe(self, **kwargs):
        r = self.s.put('/user/me', json=kwargs)
        return r

    def deleteUserMe(self):
        return self.s.delete('/user/me')

    def getUser(self, **kwargs):
        id = kwargs.get('id')
        r = self.s.get(f'/user/{id}')
        return UserSchema().load(r.json())

    def updateUser(self, **kwargs):
        id = kwargs.get('id')
        json = UserSchema.dump(kwargs.get('user'))
        return self.s.put(f'/user/{id}', json=json)

    def deleteUser(self, **kwargs):
        id = kwargs.get('id')
        return self.s.delete(f'/user/{id}')

    def updateUserMeProperties(self, **kwargs):
        id = kwargs.pop('id')
        return self.s.put(f'/user/me/properties/{id}', json=kwargs)

    def deleteUserMeProperties(self, **kwargs):
        id = kwargs.get('id')
        return self.s.delete(f'/user/me/properties/{id}')

    def swapOwner(self, **kwargs):
        return self.s.post('/swap-owner', json=kwargs)

    def getState(self):
        return self.s.post('/state').json()
