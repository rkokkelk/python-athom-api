import json

from athom.common import scopes
from athom.common.net import delete, get, post, put
from athom.managers.manager import Manager
from athom.models.managers.apps import Apps, AppsSchema

class ManagerApps(Manager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.path = "http://{homey.ip}/api/manager/apps".format(homey=self.homey)
        self.storePath = "http://{homey.ip}/api/manager/apps/store/".format(homey=self.homey)

        self.requiredScopes = [
            scopes.HOMEY_APP,
            scopes.HOMEY_APP_READONLY,
            scopes.HOMEY_APP_CONTROL
        ]


    def getApps(self):
        r = get(
            "{path}/app/".format(path=self.path),
            token=self.token
        )
        schema = AppsSchema(many=True)
        return schema.load(json.loads(r).values())


    def getApp(self, id):
        self._verify_id(id)

        r = get(
            "{path}/app/{id}".format(path=self.path, id=id),
            token=self.token
        )
        schema = AppsSchema()
        return schema.loads(r)


    def updateApp(self, id, app):
        self._verify_id(id)

        put(
            "{path}/app/{id}".format(path=self.path, id=id),
            token=self.token
        )


    def uninstallApp(self, id, purgeSettings=True):
        self._verify_id(id)

        r = delete(
            "{path}/app/{id}".format(path=self.path, id=id),
            data={'purgeSettings': purgeSettings},
            token=self.token
        )


    def getAppStd(self, id):
        self._verify_id(id)

        r = post(
            "{path}/app/{id}/crashlog".format(path=self.path, id=id),
            token=self.token
        )
        return json.loads(r)['result']


    def getAppSettings(self, id):
        self._verify_id(id)

        r = get(
            "{path}/app/{id}/settings".format(path=self.path, id=id),
            token=self.token
        )
        return json.loads(r)


    def getAppSetting(self, id, name):
        self._verify_id(id)

        r = get(
            "{path}/app/{id}/settings/{name}".format(path=self.path, id=id, name=name),
            token=self.token
        )
        return json.loads(r)['result']


    def setAppsetting(self, id, name, value):
        self._verify_id(id)

        put(
            "{path}/app/{id}/settings/{name}".format(path=self.path, id=id, name=name),
            data={'value': value},
            token=self.token
        )


    def unsetAppSetting(self, id, name):
        self._verify_id(id)

        delete(
            "{path}/app/{id}/settings/{name}".format(path=self.path, id=id, name=name),
            token=self.token
        )


    def restartApp(self, id):
        self._verify_id(id)

        post(
            "{path}/app/{id}/restart".format(path=self.path, id=id),
            token=self.token
        )


    def enableApp(self, id):
        self._verify_id(id)

        put(
            "{path}/app/{id}/enable".format(path=self.path, id=id),
            token=self.token
        )


    def disableApp(self, id):
        self._verify_id(id)

        put(
            "{path}/app/{id}/disable".format(path=self.path, id=id),
            token=self.token
        )


    def getAppLocales(self, id):
        self._verify_id(id)

        r = get(
            "{path}/app/{id}/locale".format(path=self.path, id=id),
            token=self.token
        )
        return json.loads(r)['result']


    def installFromAppStore(self, id, channel='stable'):
        self._verify_id(id)
        if channel not in ['stable', 'beta', 'alpha']:
            raise ValueError("Expected channel to be one of stable, beta, alpha")

        data = {'id': id, 'channel': channel}

        r = post(
            "{path}/store/".format(path=self.path),
            json=data,
            token=self.token
        )

        return json.loads(r)['result']
