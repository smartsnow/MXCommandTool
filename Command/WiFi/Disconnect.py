from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Disconnect from an Acess-Point.')
        return self.widget

    def encode(self):
        return cmdTable['wifi_disconnect_cmd']
