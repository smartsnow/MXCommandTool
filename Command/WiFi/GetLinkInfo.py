from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

info = Struct(
    'type' /Int8ub,
    'pointlen' /BytesInteger(2, swapped=True),
    'is_connected' /Int8ub,
    'ssid' /Bytes(32),
    'bssid' /Bytes(6),
    'security' /Int8ub,
    'channel' /Int8ub,
    'rssi' /BytesInteger(4, signed=True, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi link info.')
        return self.widget

    def encode(self):
        return cmdTable['wifi_link_info_get_cmd']

    def decode(self, cmd, payload):
        if cmd != eventTable['wifi_link_info_get_event']:
            return None

        result = info.parse(payload)
        output = ('connected: %d\r\nssid: %s\r\nbssid: %s\r\nsecurity: %d\r\nchannel: %d\r\n\rssi: %d' % (result.is_connected, result.ssid.decode(), result.bssid.hex().upper() , result.security, result.channel, result.rssi))
        return output
