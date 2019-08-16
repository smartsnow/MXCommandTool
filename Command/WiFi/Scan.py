from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Scan Access-Points around us.')
        return self.widget

    def encode(self):
        return None

    def decode(self, cmd, payload):
        return None
