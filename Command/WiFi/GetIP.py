from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get IP of Wi-Fi interface')
        self.widget.addArg('Interface', QComboBox(), 'Wi-Fi interface: SoftAP or Station')
        self.widget.getArgWidget('Interface').addItems(['Station', 'SoftAP'])
        return self.widget

    def encode(self):
        mode = self.widget.getArgWidget('Interface').currentText()
        if mode == 'SoftAP':
            return cmdTable['wifi_ip_get_cmd'] + b'\x01' + b'\x00\x00\x00\x00'
        elif mode == 'Station':
            return cmdTable['wifi_ip_get_cmd'] + b'\x01' + b'\x01\x00\x00\x00'

class Event():

    code = eventTable['wifi_ip_get_event']
    name = 'IP address'

    def decode(self, payload):
        return 'IP: %s\r\nNetMask: %s\r\nGateway: %s\r\nDns server:%s' % (payload[3:19].decode(), payload[19:35].decode(), payload[35:51].decode(), payload[51:].decode())
