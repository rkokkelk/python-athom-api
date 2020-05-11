import logging

from marshmallow import Schema, fields, post_load, EXCLUDE

log = logging.getLogger(__name__)


class Device:

    def __init__(self, id=None, **kwargs):
        self.id = id

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, obj):
        return isinstance(obj, Device) and obj.id == self.id

    def __str__(self):
        return f"[{self.zoneName}] {self.name}"

    def __repr__(self):
        return f"<Device {self}>"


class DeviceSchema(Schema):

    # Specify vars which can have None values
    icon = fields.Str(allow_none=True)
    virtualClass = fields.Str(allow_none=True)
    energy = fields.Str(allow_none=True)
    unavailableMessage = fields.Str(allow_none=True)

    class Meta:
        additional = ['id', 'name', 'driverUri', 'driverId', 'zone', 'zoneName', 'iconObj',
                      'settings', 'settingsOjb', 'class', 'energyObj',
                      'ui', 'capabilities', 'capabilitiesObj', 'capabilitiesOptions', 'flags',
                      'ready', 'available', 'repair', 'unpair', 'images',
                      'insights', 'color']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Device(**data)
