from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *
import socket

response_header = Struct(
    'type_ret' /Int8ub,
    'ret_fd' /BytesInteger(4, signed=True, swapped=True),
)

response_data = Struct(
    'type_addr' /Int8ub,
    'len_addr' /BytesInteger(2, signed=False, swapped=True)
)

sockaddr_in = Struct(
    'sin_len' /Int8ub,
    'sin_family' /Int8ub,
    'sin_port' /BytesInteger(2, signed=False, swapped=False),
    'sin_addr' /BytesInteger(4, signed=True, swapped=True),
    'sin_zero' /Bytes(8)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Accept a connection on a socket.')

        self.widget.addArg('SockFd', QLineEdit(), '[int] File descriptor for the socket.')

        return self.widget

    def encode(self):
        command = cmdTable['socket_accept_cmd']

        sock_str = self.widget.getArgWidget('SockFd').text()
        fd_input = int(sock_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + fd_input

        print(command)
        return command

class Event():

    code = eventTable['socket_accept_event']
    name = 'Event.socket.accept'

    def decode(self, payload):
        if len(payload) == response_header.sizeof():
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret_fd))
        elif len(payload) >= (response_header.sizeof() + response_data.sizeof()):
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret_fd))
            if result.ret_fd <= 0:
                return output
            else:
                data = response_data.parse(payload[response_header.sizeof():])
                index = (response_header.sizeof() + response_data.sizeof())
                addr = sockaddr_in.parse(payload[index:])
                if addr:
                    output += ('sockfd: %d\r\naddr_len: %d, addr: sin_len=%d, sin_family=%d, addr=%s, port=%d\r\n' % 
                                (result.ret_fd, data.len_addr, addr.sin_len, addr.sin_family, 
                                socket.inet_ntoa(addr.sin_addr.to_bytes(4, 'little')), addr.sin_port))
                else:
                    output += ('ERROR: response (sockaddr) format error!\r\n')
        else:
            output = ('ERROR: response format error!\r\n')

        return output
