from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *
import socket

response_header = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

response_data = Struct(
    'type' /Int8ub,
    'ip_int' /Bytes(4)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Get the IP address from a host name.')

        self.widget.addArg('Hostname', QLineEdit(), '[string] Hostname or IPv4 address in standard dot notation.')

        return self.widget

    def encode(self):
        command = cmdTable['socket_gethostbyname_cmd']

        hostname_str = self.widget.getArgWidget('Hostname').text().encode()
        command += b'\x02' + len(hostname_str).to_bytes(2, 'little') + hostname_str

        print(command)
        return command

class Event():

    code = eventTable['socket_gethostbyname_event']
    name = 'Event.socket.gethostbyname'

    def decode(self, payload):
        if len(payload) == response_header.sizeof():
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        elif len(payload) == (response_header.sizeof() + response_data.sizeof()):
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
            if result.ret < 0:
                return output
            else:
                data = response_data.parse(payload[response_header.sizeof():])
                output += ('IP: %s\r\n' % (socket.inet_ntoa(data.ip_int)))
        else:
            output = ('ERROR: response format error!\r\n')

        return output
