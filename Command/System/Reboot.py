from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Reboot Wi-Fi Module.')
        return self.widget

    def encode(self):
        return b'\x02\x10'

    def decode(self, cmd, payload):
        return None
