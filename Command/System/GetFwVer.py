from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi Module firmware version.')
        return self.widget

    def encode(self):
        return b'\x05\x10'

    def decode(self, cmd, payload):
        if cmd != b'\x04\x20':
            return None
        return payload[3:].decode()
