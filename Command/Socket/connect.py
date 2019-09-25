from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *
import socket

sa_familyDict = {'AF_NET': b'\x02', 'AF_NET6': b'\x0a'}

response_header = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

conn_addr_attr = Struct(
    'sin_len' /Bytes(1),
    'sin_family' /Bytes(1),
    'sin_port' /Bytes(2),
    'sin_addr' /Bytes(4),
    'sin_zero' /Bytes(8),
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

        Sin_family = self.widget.getArgWidget('SA_family').currentText()
        sin_family_input = sa_familyDict[Sin_family]

        ip_str = self.widget.getArgWidget('ip_addr').text()
        addr_input = socket.inet_aton(ip_str)

        port_str = self.widget.getArgWidget('port').text()
        port_input = int(port_str, base=10).to_bytes(2, 'big')

        conn_attr_len = conn_addr_attr.sizeof()
        conn_addr_cmd = conn_addr_attr.build(dict( sin_len=conn_attr_len, 
            sin_family=sin_family_input, sin_port=port_input, sin_addr=addr_input, sin_zero=0 ))
        command += b'\x02' + conn_attr_len.to_bytes(2, 'little') + conn_addr_cmd

        print(command)
        return command

class Event():

    code = eventTable['socket_connect_event']
    name = 'Event.socket.connect'

    def decode(self, payload):
        if len(payload) == response_header.sizeof():
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        else:
            output = ('ERROR: response format error!\r\n')

        return output
