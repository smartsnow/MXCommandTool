from mxArgWidgets import *

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Connect to an Acess-Point.')
        self.widget.addArg('SSID', QLineEdit(), 'SSID of an Access-Point, 1 ~ 32 characters.')
        self.widget.addArg('Passphrase', QLineEdit(), 'Passphrase of an Access-Point, 8 ~ 63 characters.')
        return self.widget

    def encode(self):
        return None

    def decode(self, cmd, payload):
        return None
