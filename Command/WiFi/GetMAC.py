from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi MAC address.')
        return self.widget

    def encode(self):
        return b'\x11\x10'

    def decode(self, cmd, payload):
        if cmd != b'\x0a\x20':
            return None
        return 'MAC address: %s' % (payload[3:].hex().upper())
