from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget("Get Wi-Fi module's version.")
        return self.widget

    def encode(self):
        return b'\x03\x10'

    def decode(self, cmd, payload):
        if cmd != b'\x02\x20':
            return None
        return 'Version: %s' % (payload[3:].decode())
