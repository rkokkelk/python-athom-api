import json

from athom.common import scopes
from athom.common.net import delete, get, post, put
from athom.managers.manager import Manager
from athom.models.managers.apps import Apps, AppsSchema

class ManagerDevices(Manager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.path = "http://{homey.ip}/api/manager/devices".format(homey=self.homey)

        self.requiredScopes = [
            scopes.HOMEY_DEVICE,
            scopes.HOMEY_DEVICE_READONLY,
            scopes.HOMEY_DEVICE_CONTROL
        ]


    def getDevices(self):
        raise NotImplementedError()


    def getDevice(self, id):
        raise NotImplementedError()


    def updateDevice(self, id, device):
        raise NotImplementedError()


    def deletDevice(self, id):
        raise NotImplementedError()


    def setCapabilityValue(self, deviceId, capabilityId, value, **kwargs):
        raise NotImplementedError()

    def getDeviceSettingsObj(self, id):
        raise NotImplementedError()


    def setDeviceSettings(self, id, settings):
        raise NotImplementedError()


    def getCapabilities(self):
        raise NotImplementedError()


    def getCapability(self, uri, id):
        raise NotImplementedError()
