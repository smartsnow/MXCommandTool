from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *
import socket

flagDict = {'DEFAULT': b'\x00\x00\x00\x00'}

response_header = Struct(
    'type_ret' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True),
)

response_data = Struct(
    'type_sockfd' /Int8ub,
    'sockfd' /BytesInteger(4, signed=True, swapped=True),
    'type_data' /Int8ub,
    'len_data' /BytesInteger(2, signed=False, swapped=True)
)

sockaddr_in = Struct(
    'sin_len' /Int8ub,
    'sin_family' /Int8ub,
    'sin_port' /BytesInteger(2, signed=False, swapped=True),
    'sin_addr' /BytesInteger(4, signed=True, swapped=True),
    'sin_zero' /Bytes(8)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Socket recvfrom.')

        self.widget.addArg('SockFd', QLineEdit(), '[int] File descriptor for the socket.')
        self.widget.addArg('Size', QLineEdit(), '[int] lenght to receive.')
        self.widget.addArg('flag', QComboBox(), 'Option flag.')
        self.widget.getArgWidget('flag').addItems(['DEFAULT'])

        return self.widget

    def encode(self):
        command = cmdTable['socket_recvfrom_cmd']

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

    code = eventTable['socket_recvfrom_event']
    name = 'Event.socket.recvfrom'

    def decode(self, payload):
        if len(payload) == response_header.sizeof():
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        elif len(payload) >= (response_header.sizeof() + response_data.sizeof()):
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
            if result.ret <= 0:
                return output
            else:
                index = response_header.sizeof()
                data = response_data.parse(payload[index:(index+response_data.sizeof())])
                index += response_data.sizeof()
                if len(payload) >= (response_header.sizeof() + response_header.sizeof() + data.len_data):
                    data_recv = payload[index:(index+data.len_data)].hex()
                    index += data.len_data
                    if len(payload) == (response_header.sizeof() + response_data.sizeof() + data.len_data + 3 + sockaddr_in.sizeof()):
                        addr = sockaddr_in.parse(payload[(index+3):])
                        output += ('sockfd: %d\r\nlen: %d\r\ndata: b\'%s\'\r\naddr: sin_len=%d, sin_family=0x%04x, addr=%s, port=%d\r\n' % 
                                    (data.sockfd, 
                                    data.len_data, data_recv, 
                                    addr.sin_len, addr.sin_family, 
                                    socket.inet_ntoa(addr.sin_addr.to_bytes(4, 'little')),
                                    addr.sin_port))
                    else:
                        output += ('ERROR: response (sockaddr) format error!\r\n')
                else:
                    output += ('ERROR: response (data len) format error!\r\n')
        else:
            output = ('ERROR: response format error!\r\n')

        return output
