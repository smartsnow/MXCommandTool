from mxArgWidgets import *
from cmdTable import cmdTable, eventTable


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi MAC address.')
        return self.widget

    def encode(self):
        return cmdTable['wifi_mac_get_cmd']

class Event():
    
    code = eventTable['wifi_mac_get_event']
    name = 'MAC Address'

    def decode(self, payload):
        return payload[3:].hex().upper()
