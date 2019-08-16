from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Send data on a socket.')
        self.widget.addArg('FD', QLineEdit(), 'File Descriptor of a socket.')
        self.widget.addArg('Data', MxHexStrEdit(), 'Data to be sent on a socket.')
        return self.widget

    def encode(self):
        return None

    def decode(self, cmd, payload):
        return None
