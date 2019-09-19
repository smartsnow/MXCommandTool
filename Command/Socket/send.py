from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

flagDict = {'DEFAULT': b'\x00\x00\x00\x00'}

response_header = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Socket send.')

        self.widget.addArg('SockFd', QLineEdit(), '[int] File descriptor for the socket.')
        self.widget.addArg('data', QPlainTextEdit(), '[string] Data to send.')
        self.widget.addArg('flag', QComboBox(), 'Option flag.')
        self.widget.getArgWidget('flag').addItems(['DEFAULT'])

        return self.widget

    def encode(self):
        command = cmdTable['socket_send_cmd']

        sockfd_str = self.widget.getArgWidget('SockFd').text()
        fd_input = int(sockfd_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + fd_input

        data_input = self.widget.getArgWidget('data').toPlainText().encode()
        command += b'\x02' + len(data_input).to_bytes(2, 'little') + data_input

        flag = self.widget.getArgWidget('flag').currentText()
        flag_input = flagDict[flag]
        command += b'\x01' + flag_input

        print(command)
        return command

class Event():

    code = eventTable['socket_send_event']
    name = 'Event.socket.send'

    def decode(self, payload):
        if len(payload) == response_header.sizeof():
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        else:
            output = ('ERROR: response format error!\r\n')

        return output
