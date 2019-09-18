from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

sa_familyDict = {'AF_NET': b'\x02\x00\x00\x00', 'AF_NET6': b'\x0a\x00\x00\x00'}

response = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Socket listen.')

        self.widget.addArg('SockFd', QLineEdit(), '[int] File descriptor for the socket.')
        self.widget.addArg('Max', QLineEdit(), '[int, use 0 is fine] max lenght of pending connections queue.')

        return self.widget

    def encode(self):
        command = cmdTable['socket_listen_cmd']

        sock_str = self.widget.getArgWidget('SockFd').text()
        fd_input = int(sock_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + fd_input

        max_str = self.widget.getArgWidget('Max').text()
        max_input = int(max_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + max_input

        print(command)
        return command

class Event():

    code = eventTable['socket_listen_event']
    name = 'Event.socket.listen'

    def decode(self, payload):
        result = response.parse(payload)
        output = ('return: %d\r\n' % (result.ret))
        return output
