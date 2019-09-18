from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

flagDict = {'DEFAULT': b'\x00\x00\x00\x00'}

response_ret = Struct(
    'type_ret' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True),
)

response = Struct(
    'type_sockfd' /Int8ub,
    'sockfd' /BytesInteger(4, signed=True, swapped=True),
    'type_data' /Int8ub,
    'len_data' /BytesInteger(2, signed=False, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Socket recv.')

        self.widget.addArg('SockFd', QLineEdit(), '[int] File descriptor for the socket.')
        self.widget.addArg('Size', QLineEdit(), '[int] lenght to receive.')
        self.widget.addArg('flag', QComboBox(), 'Option flag.')
        self.widget.getArgWidget('flag').addItems(['DEFAULT'])

        return self.widget

    def encode(self):
        command = cmdTable['socket_recv_cmd']

        sockfd_str = self.widget.getArgWidget('SockFd').text()
        fd_input = int(sockfd_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + fd_input

        size_str = self.widget.getArgWidget('Size').text()
        size_input = int(size_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + size_input

        flag = self.widget.getArgWidget('flag').currentText()
        flag_input = flagDict[flag]
        command += b'\x01' + flag_input

        print(command)
        return command

class Event():

    code = eventTable['socket_recv_event']
    name = 'Event.socket.recv'

    def decode(self, payload):
        if len(payload) == response_ret.sizeof():
            result = response_ret.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        else:
            result = response.parse(payload)
            index = response.sizeof()
            data = payload[index:].hex()
            output = ('sockfd: %d\r\nlen: %d\r\ndata: %s\r\n' % 
                        (result.sockfd, result.len_data, data))
        return output
