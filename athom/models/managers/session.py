import logging

from marshmallow import Schema, post_load, EXCLUDE

log = logging.getLogger(__name__)


class Session:

    def __init__(self, id=None, **kwargs):
        self.id = id
        self.type = kwargs.pop('type', None)
        self.scopes = kwargs.pop('scopes', list())

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, obj):
        return isinstance(obj, Session) and obj.id == self.id

    def __str__(self):
        return f"[{self.type}] {self.scopes}"

    def __repr__(self):
        return f"<Session {self}>"

    def hasScope(self, scope):
        return scope in self.scopes

    def hasScopes(self, scopes):
        return all([scope in self.scopes for scope in scopes])


class SessionSchema(Schema):

    class Meta:
        additional = ['id', 'type', 'agent', 'scopes', 'intersectedScopes', 'createdAt',
                      'expiresAt', 'lastUsed']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Session(**data)
