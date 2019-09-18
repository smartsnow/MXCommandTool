from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

sa_familyDict = {'AF_NET': b'\x02\x00\x00\x00', 'AF_NET6': b'\x0a\x00\x00\x00'}

response = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

conn_addr_attr = Struct(
    'sa_family' /Bytes(4),
    'ip' /Bytes(16),
    'port' /BytesInteger(4, signed=True, swapped=True),
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Socket connect.')

        self.widget.addArg('SockFd', QLineEdit(), '[int] File descriptor for the socket.')
        self.widget.addArg('SA_family', QComboBox(), 'SA_Family.')
        self.widget.getArgWidget('SA_family').addItems(['AF_NET', 'AF_NET6'])
        self.widget.addArg('ip_addr', QLineEdit(), '[string] IP address.')
        self.widget.addArg('port', QLineEdit(), '[int] port.')

        return self.widget

    def encode(self):
        command = cmdTable['socket_connect_cmd']

        sock_str = self.widget.getArgWidget('SockFd').text()
        fd_input = int(sock_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + fd_input

        SA_family = self.widget.getArgWidget('SA_family').currentText()
        sa_family_input = sa_familyDict[SA_family]

        ip_input = self.widget.getArgWidget('ip_addr').text().encode()
        ip_input += (16 - len(ip_input)) * b'\x00'

        port_str = self.widget.getArgWidget('port').text()
        port_input = int(port_str, base=10)

        conn_attr_len = conn_addr_attr.sizeof()
        conn_addr_cmd = conn_addr_attr.build(dict( sa_family=sa_family_input, ip=ip_input, port=port_input ))
        command += b'\x02' + conn_attr_len.to_bytes(2, 'little') + conn_addr_cmd

        print(command)
        return command

class Event():

    code = eventTable['socket_connect_event']
    name = 'Event.socket.connect'

    def decode(self, payload):
        result = response.parse(payload)
        output = ('return: %d\r\n' % (result.ret))
        return output
