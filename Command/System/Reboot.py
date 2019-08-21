from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Reboot Wi-Fi Module.')
        return self.widget

    def encode(self):
        return cmdTable['system_reboot_cmd']
