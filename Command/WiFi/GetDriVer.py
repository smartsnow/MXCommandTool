from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget("Get Wi-Fi module's driver version.")
        return self.widget

    def encode(self):
        return cmdTable['wifi_version_get_cmd']

    def decode(self, cmd, payload):
        if cmd != eventTable['wifi_version_get_event']:
            return None
        return payload[3:].decode()
