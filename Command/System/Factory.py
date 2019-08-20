from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Factory Wi-Fi Module.')
        return self.widget

    def encode(self):
        return cmdTable['system_factory_cmd']

    def decode(self, cmd, payload):
        return None
