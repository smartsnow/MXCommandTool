from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Send data on a socket.')
        self.widget.addArg('FD', QLineEdit(), 'File Descriptor of a socket.')
        self.widget.addArg('Data', MxHexStrEdit(), 'Data to be sent on a socket.')
        return self.widget

    def getArgs(self):
        return {'FD': self.widget.getArgWidget('FD').text(), 'Data': self.widget.getArgWidget('Data').text()}

    def parse(self, data):
        pass
