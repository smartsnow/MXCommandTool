from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi Module firmware version.')
        return self.widget

    def encode(self):
        return cmdTable['system_firmware_version_get_cmd']

class Event():

    code = eventTable['system_firmware_version_get_event']
    name = 'Firmware Version'

    def decode(self, payload):
        return payload[3:].decode()
