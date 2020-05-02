import json

from athom.common import scopes
from athom.managers.manager import Manager
from athom.models.managers.apps import Apps, AppsSchema

class ManagerApps(Manager):

    def __init__(self, **kwargs):
        super().__init__(base="/apps", **kwargs)

        self.requiredScopes = [
            scopes.HOMEY_APP,
            scopes.HOMEY_APP_READONLY,
            scopes.HOMEY_APP_CONTROL
        ]


    def getApps(self):
        r = self.s.get('/app/')
        schema = AppsSchema(many=True)
        return schema.load(json.loads(r).values())


    def getApp(self, id):
        self._verify_id(id)

        r = self.s.get(f"/app/{id}")
        schema = AppsSchema()
        return schema.loads(r)


    def updateApp(self, id, app):
        self._verify_id(id)
        self.s.put(f"/app/{id}")


    def uninstallApp(self, id, purgeSettings=True):
        self._verify_id(id)
        self.s.delete(f"/app/{id}", data={'purgeSettings': purgeSettings})


    def getAppStd(self, id):
        self._verify_id(id)

        r = self.s.post(f"/app/{id}/crashlog")
        return r.json().get('result')


    def getAppSettings(self, id):
        self._verify_id(id)

        r = self.s.get(f"/app/{id}/settings")
        return r.json()


    def getAppSetting(self, id, name):
        self._verify_id(id)

        r = self.s.get(f"/app/{id}/settings/{name}")
        return r.json().get('result')


    def setAppsetting(self, id, name, value):
        self._verify_id(id)
        self.s.put(f"/app/{id}/settings/{name}", data={'value': value})


    def unsetAppSetting(self, id, name):
        self._verify_id(id)
        self.s.delete(f"/app/{id}/settings/{name}")


    def restartApp(self, id):
        self._verify_id(id)
        self.s.post(f"/app/{id}/restart")


    def enableApp(self, id):
        self._verify_id(id)
        self.s.put(f"/app/{id}/enable")


    def disableApp(self, id):
        self._verify_id(id)
        self.s.put(f"/app/{id}/disable")


    def getAppLocales(self, id):
        self._verify_id(id)

        r = self.s.get(f"/app/{id}/locale")
        return r.json().get('result')


    def installFromAppStore(self, id, channel='stable'):
        self._verify_id(id)
        if channel not in ['stable', 'beta', 'alpha']:
            raise ValueError("Expected channel to be one of stable, beta, alpha")

        r = self.s.post('/store/', json={'id': id, 'channel': channel})
        return r.json().get('result')
