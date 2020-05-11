from athom.common import scopes
from athom.managers.manager import Manager
from athom.models.managers.devices import DeviceSchema
from athom.models.managers.capabilities import CapabilitySchema


class ManagerDevices(Manager):

    def __init__(self, **kwargs):
        super().__init__(base='/devices', **kwargs)

        self.requiredScopes = [
            scopes.HOMEY_DEVICE,
            scopes.HOMEY_DEVICE_READONLY,
            scopes.HOMEY_DEVICE_CONTROL
        ]

    def getDevices(self):
        r = self.s.get('/device/')
        schema = DeviceSchema(many=True)
        return schema.load(r.json().values())

    def getDevice(self, **opts):
        id = opts.get('id')
        r = self.s.get(f'/device/{id}')
        return DeviceSchema().load(r.json())

    def updateDevice(self, **opts):
        id = opts.get('id')
        return self.s.put(f'/device/{id}')

    def deleteDevice(self, **opts):
        id = opts.get('id')
        return self.s.delete(f'/device/{id}')

    def setCapabilityValue(self, **opts):
        deviceId = opts.pop('deviceId')
        capabilityId = opts.pop('capabilityId')
        return self.s.put(f'/device/{deviceId}/capability/{capabilityId}', json=opts)

    def getDeviceSettingsObj(self, **opts):
        id = opts.get('id')
        return self.s.get(f'/device/{id}/settings_obj')

    def setDeviceSettings(self, **opts):
        id = opts.pop('id')
        return self.s.put(f'/device/{id}/settings', json=opts)

    def getCapabilities(self, **opts):
        r = self.s.get('/capability', params=opts)
        schema = CapabilitySchema(many=True)
        return schema.load(r.json())

    def getCapability(self, **opts):
        id = opts.get('id')
        uri = opts.get('uri')

        r = self.s.get(f'/capability/{uri}/{id}')
        return CapabilitySchema().load(r.json())
