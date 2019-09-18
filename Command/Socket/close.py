from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

response = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Socket close.')

        self.widget.addArg('Filedes', QLineEdit(), '[int] File descriptor for the socket.')

        return self.widget

    def encode(self):
        command = cmdTable['socket_close_cmd']

        sock_str = self.widget.getArgWidget('Filedes').text()
        fd_input = int(sock_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + fd_input

        print(command)
        return command

class Event():

    code = eventTable['socket_close_event']
    name = 'Event.socket.close'

    def decode(self, payload):
        result = response.parse(payload)
        output = ('return: %d\r\n' % (result.ret))
        return output
