from mxArgWidgets import *
from ctypes import *


class wifi_info(Structure):
    _fields_ = [('is_connected', c_uint8),
                ('ssid', c_char*33),
                ('bssid', c_uint8*6),
                ('channel', c_uint8),
                ('rssi', c_int)]

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get Wi-Fi link info.')
        return self.widget

    def encode(self):
        return b'\x15\x10'

    def decode(self, cmd, payload):
        if cmd != b'\x0d\x20':
            return None
        info = wifi_info()
        info.is_connected = payload[3]
        info.ssid = payload[4:36]
        # info.bssid = payload[36:41]
        info.channel = payload[41]
        # info.rssi = int(payload[42:])
        return 'WiFi(%d)\r\nssid(%s)\r\nchannel(%d)' % (info.is_connected, info.ssid.decode(), info.channel)
