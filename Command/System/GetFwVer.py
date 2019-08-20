from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi Module firmware version.')
        return self.widget

    def encode(self):
        return cmdTable['system_firmware_version_get_cmd']

    def decode(self, cmd, payload):
        if cmd != eventTable['system_firmware_version_get_event']:
            return None
        return payload[3:].decode()
