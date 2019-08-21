from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

ip_attr = Struct(
    'localip' /Bytes(16),
    'netmask' /Bytes(16),
    'gateway' /Bytes(16),
    'dnserver' /Bytes(16),
)

connect_attr = Struct(
    'bssid' /Bytes(6),
    'channel' /Int8ub,
    'security' /Int8ub,
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Connect to an Acess-Point.')
        self.widget.addArg('SSID', QLineEdit(), 'SSID of an Access-Point, 1 ~ 32 characters.')
        self.widget.addArg('Passphrase', QLineEdit(), 'Passphrase of an Access-Point, 8 ~ 63 characters.')
        self.widget.addArg('DHCP', QComboBox(), 'Wi-Fi interface: Enable or Disable')
        self.widget.getArgWidget('DHCP').addItems(['Enable', 'Disable'])
        self.widget.addArg('LocalIP', QLineEdit(), 'lcoal ip address.')
        self.widget.addArg('Netmask', QLineEdit(), 'netmask.')
        self.widget.addArg('Gateway', QLineEdit(), 'gateway ip address.')
        self.widget.addArg('Dnserver', QLineEdit(), 'dns server ip address.')
        self.widget.addArg('Advanced', QComboBox(), 'Wi-Fi interface: Advanced option')
        self.widget.getArgWidget('Advanced').addItems(['Disable', 'Enable'])
        self.widget.addArg('Bssid', QLineEdit(), 'Bssid.')
        self.widget.addArg('Channel', QComboBox(), 'Wi-Fi interface: Advanced option')
        self.widget.getArgWidget('Channel').addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'])
        self.widget.addArg('Security', QComboBox(), 'Wi-Fi interface: Advanced option')
        self.widget.getArgWidget('Security').addItems(['NONE', 'WEP', 'WPA_TKIP', 'WPA_AES', 'WPA2_TKIP', 'WPA2_AES', 'WPA2_MIXED', 'AUTO'])

        return self.widget

    def encode(self):
        ssidinput = self.widget.getArgWidget('SSID').text().encode()
        ssidlen = len(ssidinput)
        keyinput = self.widget.getArgWidget('Passphrase').text().encode()
        keylen = len(keyinput)

        command = cmdTable['wifi_connect_cmd'] + b'\x02' + ssidlen.to_bytes(2, 'little') + ssidinput + b'\x02' + keylen.to_bytes(2, 'little') + keyinput
    
        dhcp_status = self.widget.getArgWidget('DHCP').currentText()
        adv_status = self.widget.getArgWidget('Advanced').currentText()

        if adv_status == 'Disable':
            command += (b'\x02' + b'\x01\x00' + b'\x00')
        elif adv_status == 'Enable':
            command += (b'\x02' + b'\x01\x00' + b'\x00')

        if dhcp_status == 'Enable':
            command += b'\x02' + b'\x01\x00' + b'\x00'
            return command
        elif dhcp_status == 'Disable':
            localipinput = self.widget.getArgWidget('LocalIP').text().encode()
            localipinput += (16 - len(localipinput)) * b'\x00'
            netmaskinput = self.widget.getArgWidget('Netmask').text().encode()
            netmaskinput += (16 - len(netmaskinput)) * b'\x00'
            gatewayinput = self.widget.getArgWidget('Gateway').text().encode()
            gatewayinput += (16 - len(gatewayinput)) * b'\x00'
            dnserverinput = self.widget.getArgWidget('Dnserver').text().encode()
            dnserverinput += (16 - len(dnserverinput)) * b'\x00'

            ipattrlen = ip_attr.sizeof()

            ipcmd = ip_attr.build(dict( localip=localipinput, netmask=netmaskinput, gateway=gatewayinput, dnserver=dnserverinput ))

            command += b'\x02' + ipattrlen.to_bytes(2, 'little') + ipcmd
            print(command)
            return command
