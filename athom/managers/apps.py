from athom.common import scopes
from athom.common.net import get, post
from athom.managers.manager import Manager

class ManagerApps(Manager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.homeyPath = "http://{homey.ip}/api/manager/apps/app".format(homey=self.homey)
        self.requiredScopes = [
            scopes.HOMEY_APP,
            scopes.HOMEY_APP_READONLY,
            scopes.HOMEY_APP_CONTROL
        ]


    def getApps(self):
        return get(self.homeyPath, token=self.token)


    def getApp(self, id):
        NotImplementedError()


    def updateApp(self, id, app):
        NotImplementedError()


    def uninstallApp(self, id, purgeSettings=False):
        NotImplementedError()


    def getAppStd(self, id):
        NotImplementedError()


    def getAppSettings(self, id):
        NotImplementedError()


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
