from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Connect to an Acess-Point.')
        self.widget.addArg('SSID', QLineEdit(), 'SSID of an Access-Point, 1 ~ 32 characters.')
        self.widget.addArg('Passphrase', QLineEdit(), 'Passphrase of an Access-Point, 8 ~ 63 characters.')
        return self.widget

    def encode(self):
        ssidinput = self.widget.getArgWidget('SSID').text().encode()
        ssidlen = len(ssidinput)
        keyinput = self.widget.getArgWidget('Passphrase').text().encode()
        keylen = len(keyinput)
        command = cmdTable['wifi_connect_cmd'] + b'\x02' + ssidlen.to_bytes(2, 'little') + ssidinput + b'\x02' + keylen.to_bytes(2, 'little') + keyinput 
        return command

    def decode(self, cmd, payload):
        return None
