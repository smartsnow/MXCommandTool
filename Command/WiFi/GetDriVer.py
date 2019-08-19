from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget("Get Wi-Fi module's driver version.")
        return self.widget

    def encode(self):
        return b'\x10\x10'

    def decode(self, cmd, payload):
        if cmd != b'\x09\x20':
            return None
        return payload[3:].decode()
