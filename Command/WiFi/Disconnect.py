from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Disconnect from an Acess-Point.')
        return self.widget

    def encode(self):
        return None

    def decode(self, cmd, payload):
        return None
