from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi MAC address.')
        return self.widget

    def encode(self):
        return b'\x04\x10'

    def decode(self, cmd, payload):
        if cmd != b'\x03\x20':
            return None
        return 'MAC address: %s' % (payload[3:].hex().upper())
