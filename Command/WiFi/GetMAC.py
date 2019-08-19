from mxArgWidgets import *
from cmdTable import cmdTable, eventTable


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi MAC address.')
        return self.widget

    def encode(self):
        return cmdTable['wifi_mac_get_cmd']

    def decode(self, cmd, payload):
        if cmd != eventTable['wifi_mac_get_event']:
            return None
        return 'MAC address: %s' % (payload[3:].hex().upper())
