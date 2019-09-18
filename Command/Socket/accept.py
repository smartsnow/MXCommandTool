from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *
import socket

response_ret = Struct(
    'type_ret' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True),
)

response = Struct(
    'type_sockfd' /Int8ub,
    'sockfd' /BytesInteger(4, signed=True, swapped=True),
    'type_addr' /Int8ub,
    'len_addr' /BytesInteger(2, signed=False, swapped=True)
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
        if len(payload) == response_ret.sizeof():
            result = response_ret.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        else:
            result = response.parse(payload)
            index = response.sizeof()
            # addr = payload[index:].hex()
            addr = sockaddr_in.parse(payload[index:])
            output = ('sockfd: %d\r\naddr: sin_len=%d, sin_family=0x%02x, addr=%s, port=%d\r\n' % 
                        (result.sockfd, addr.sin_len, addr.sin_family, 
                        socket.inet_ntoa(addr.sin_addr.to_bytes(4, 'little')), addr.sin_port))
        return output
