from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *
import socket

response = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
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
        result = response.parse(payload)
        if result.ret < 0:
            output = ('return: %d\r\n' % (result.ret))
        else:
            output = ('IP: %s\r\n' % (socket.inet_ntoa(result.ret.to_bytes(4, 'little'))))

        return output
