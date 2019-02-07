import json

from athom.common import scopes
from athom.common.net import delete, get, post
from athom.managers.manager import Manager
from athom.models.managers.apps import Apps, AppsSchema

class ManagerApps(Manager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.homeyPath = "{homey.url}/api/manager/apps/app".format(homey=self.homey)
        self.requiredScopes = [
            scopes.HOMEY_APP,
            scopes.HOMEY_APP_READONLY,
            scopes.HOMEY_APP_CONTROL
        ]


    def getApps(self):
        r = get(self.homeyPath, token=self.token)
        print(r)
        schema = AppsSchema(many=True)
        return schema.load(json.loads(r).values())


    def getApp(self, id):
        r = get(
            "{path}/{id}".format(path=self.homeyPath, id=id),
            token=self.token
        )
        schema = AppsSchema()
        return schema.loads(r)


    def updateApp(self, id, app):
        NotImplementedError()


    def uninstallApp(self, id, purgeSettings=True):
        r = delete(
            "{path}/{id}".format(path=self.homeyPath, id=id),
            data={'purgeSettings': purgeSettings},
            token=self.token
        )


    def getAppStd(self, id):
        r = post(
            "{path}/{id}/crashlog".format(path=self.homeyPath, id=id),
            token=self.token
        )
        return json.loads(r)['result']


    def getAppSettings(self, id):
        r = get(
            "{path}/{id}/setting".format(path=self.homeyPath, id=id),
            token=self.token
        )
        return json.loads(r)


    def getAppSetting(self, id, name):
        NotImplementedError()


    def setappsetting(self, id, name, value):
        NotImplementedError()


    def unsetAppSetting(self, id, name):
        NotImplementedError()


    def restartApp(self, id):
        NotImplementedError()


    def enableApp(self, id):
        NotImplementedError()


    def getAppLocales(self, id):
        NotImplementedError()


    def installFromAppStore(self, id, channel):
        NotImplementedError()
