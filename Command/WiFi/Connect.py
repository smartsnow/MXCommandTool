from mxArgWidgets import *

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Connect to an Acess-Point.')
        self.widget.addArg('SSID', QLineEdit(), 'SSID of an Access-Point, 1 ~ 32 characters.')
        self.widget.addArg('Passphrase', QLineEdit(), 'Passphrase of an Access-Point, 8 ~ 63 characters.')
        return self.widget

    def getArgs(self):
        return {'SSID': self.widget.getArgWidget('SSID').text(), 'Passphrase': self.widget.getArgWidget('Passphrase').text()}

    def parse(self, data):
        pass
