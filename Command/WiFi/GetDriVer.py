from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget("Get Wi-Fi module's driver version.")
        return self.widget

    def encode(self):
        return cmdTable['wifi_version_get_cmd']

class Event():

    code = eventTable['wifi_version_get_event']
    name = 'Driver Version'

    def decode(self, payload):
        return payload[3:].decode()
