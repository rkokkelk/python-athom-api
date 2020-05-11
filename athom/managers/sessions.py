import logging

from athom.managers.manager import Manager
from athom.models.managers.session import SessionSchema

log = logging.getLogger(__name__)


class ManagerSessions(Manager):

    def __init__(self, **kwargs):
        super().__init__(base='/sessions', **kwargs)

        self.requiredScopes = []

    def getSessions(self):
        r = self.s.get('/session')
        schema = SessionSchema(many=True)
        return schema.loads(r.json())

    def getSessionMe(self):
        r = self.s.get('/session/me')
        return SessionSchema.loads(r)

    def deleteSession(self, **opts):
        id = opts.get('id')
        return self.s.delete(f'/session/{id}')
