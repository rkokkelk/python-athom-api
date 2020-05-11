from athom.common import scopes
from athom.managers.manager import Manager
from athom.models.managers.apps import AppsSchema


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
        return schema.load(r.json())

    def getApp(self, **opts):
        id = opts.get('id')
        self._verify_id(id)

        r = self.s.get(f"/app/{id}")
        return AppsSchema().loads(r.json())

    def updateApp(self, **opts):
        id = opts.get('id')
        self._verify_id(id)
        return self.s.put(f"/app/{id}")

    def uninstallApp(self, **opts):
        id = opts.pop('id')
        self._verify_id(id)
        return self.s.delete(f"/app/{id}", json=opts)

    def getAppStd(self, **opts):
        id = opts.pop('id')
        self._verify_id(id)

        r = self.s.post(f"/app/{id}/crashlog", json=opts)
        return r.json().get('result')

    def getAppSettings(self, **opts):
        id = opts.get('id')
        self._verify_id(id)

        r = self.s.get(f"/app/{id}/settings")
        return r.json()

    def getAppSetting(self, **opts):
        id = opts.get('id')
        name = opts.get('name')
        self._verify_id(id)

        r = self.s.get(f"/app/{id}/settings/{name}")
        return r.json().get('result')

    def setAppsetting(self, **opts):
        id = opts.pop('id')
        name = opts.pop('name')

        self._verify_id(id)
        return self.s.put(f"/app/{id}/settings/{name}", json=opts)

    def unsetAppSetting(self, **opts):
        id = opts.get('id')
        name = opts.get('name')
        self._verify_id(id)
        return self.s.delete(f"/app/{id}/settings/{name}")

    def restartApp(self, **opts):
        id = opts.get('id')
        self._verify_id(id)
        return self.s.post(f"/app/{id}/restart")

    def garbageCollectApp(self, **opts):
        raise NotImplementedError()

    def enableApp(self, **opts):
        id = opts.get('id')
        self._verify_id(id)
        return self.s.put(f"/app/{id}/enable")

    def disableApp(self, **opts):
        id = opts.get('id')
        self._verify_id(id)
        return self.s.put(f"/app/{id}/disable")

    def getAppLocales(self, **opts):
        id = opts.get('id')
        self._verify_id(id)

        r = self.s.get(f"/app/{id}/locale")
        return r.json().get('result')

    def installFromAppStore(self, **opts):
        id = opts.get('id')
        self._verify_id(id)

        if opts.get('channel') not in ['stable', 'beta', 'alpha']:
            raise ValueError("Expected channel to be one of stable, beta, alpha")

        r = self.s.post('/store/', json=opts)
        return r.json().get('result')

    def destroy():
        raise NotImplementedError()
