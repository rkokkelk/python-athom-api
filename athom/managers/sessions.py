import json
import logging

from athom.common import scopes
from athom.common.net import delete, get, post
from athom.managers.manager import Manager
from athom.models.managers.session import Session, SessionSchema

log = logging.getLogger(__name__)


class ManagerSessions(Manager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.homeyPath = "{homey.url}/api/manager/sessions".format(homey=self.homey)
        self.requiredScopes = []


    def getSessions(self):
        url = self.homeyPath + '/session'

        r = get(url, token=self.token)
        schema = SessionSchema(many=True)
        return schema.loads(r)


    def getSessionMe(self):
        url = self.homeyPath + '/session/me'

        r = get(url, token=self.token)
        log.debug(r)
        schema = SessionSchema()
        return schema.loads(r)




    def deleteSession(self):
        raise NotImplementedError()

