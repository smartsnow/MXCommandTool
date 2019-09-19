from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

response_header = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Socket shutdown.')

        self.widget.addArg('Filedes', QLineEdit(), '[int] File descriptor for the socket.')
        self.widget.addArg('How', QLineEdit(), '[int] 0: Stop receiving data for this socket;\r\n1: Stop trying to transmit data from this socket.')

        return self.widget

    def encode(self):
        command = cmdTable['socket_shutdown_cmd']

        sock_str = self.widget.getArgWidget('Filedes').text()
        fd_input = int(sock_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + fd_input

        how_str = self.widget.getArgWidget('How').text()
        how_input = int(how_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + how_input

        print(command)
        return command

class Event():

    code = eventTable['socket_shutdown_event']
    name = 'Event.socket.shutdown'

    def decode(self, payload):
        if len(payload) == response_header.sizeof():
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        else:
            output = ('ERROR: response format error!\r\n')

        return output
