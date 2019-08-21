from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Send data on a socket.')
        self.widget.addArg('FD', QLineEdit(), 'File Descriptor of a socket.')
        self.widget.addArg('Data', MxHexStrEdit(), 'Data to be sent on a socket.')
        return self.widget

    def encode(self):
        return None

class Event():

    code = None
    name = None

    def decode(self, payload):
        return None
