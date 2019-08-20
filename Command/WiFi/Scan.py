from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

data = Struct(
    'type1' /Int8ub,
    'ap_num' /BytesInteger(4, swapped=True),
    'type2' /Int8ub,
    'pointlen' /BytesInteger(2, swapped=True),
)

apinfo = Struct(
    'ssid' /Bytes(32),
    'bssid' /Bytes(6),
    'security' /Int8ub,
    'channel' /Int8ub,
    'rssi' /BytesInteger(4, signed=True, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Scan Access-Points around us.')
        self.widget.addArg('ScanMode', QComboBox(), 'Wi-Fi Scan: Normal or Activate')
        self.widget.getArgWidget('ScanMode').addItems(['Normal', 'Activate'])
        self.widget.addArg('SSID', QLineEdit(), 'SSID of an Access-Point, 1 ~ 32 characters.')
        return self.widget

    def encode(self):
        mode = self.widget.getArgWidget('ScanMode').currentText()
        ssidinput = self.widget.getArgWidget('SSID').text().encode()
        ssidlen = len(ssidinput)
        if mode == 'Normal':
            return cmdTable['wifi_scan_cmd'] + b'\x01' + b'\x00\x00\x00\x00'
        elif mode == 'Activate':
            return  cmdTable['wifi_scan_cmd'] + b'\x01' + b'\x01\x00\x00\x00' + b'\x02' + ssidlen.to_bytes(2, 'little') + ssidinput


    def decode(self, cmd, payload):        
        if cmd != eventTable['wifi_scan_event']:
            return None

        data_parse = data.parse(payload)

        index = data.sizeof()
        apinfo_parse = []
        output = ''
        for i in range(0, data_parse.ap_num):
            apinfo_parse.append(apinfo.parse(payload[index:]))
            index += apinfo.sizeof()
            output += ( '%s\t %d\t %d\t %s\r\n' % (apinfo_parse[i].bssid.hex().upper(), apinfo_parse[i].rssi, apinfo_parse[i].channel, apinfo_parse[i].ssid.decode() ) )
        
        return output
