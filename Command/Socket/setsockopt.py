from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

levelDict = {
    'SOL_SOCKET': b'\xff\x0f\x00\x00', 
    'IPPROTO_IP': b'\x00\x00\x00\x00', 
    'IPPROTO_TCP': b'\x06\x00\x00\x00', 
    'IPPROTO_UDP': b'\x11\x00\x00\x00'
}

optnameDict = {
    'SO_DEBUG': b'\x01\x00\x00\x00', 
    'SO_ACCEPTCONN': b'\x02\x00\x00\x00', 
    'SO_REUSEADDR': b'\x04\x00\x00\x00', 
    'SO_KEEPALIVE': b'\x08\x00\x00\x00',
    'SO_DONTROUTE': b'\x10\x00\x00\x00',
    'SO_BROADCAST': b'\x20\x00\x00\x00',
    'SO_USELOOPBACK': b'\x40\x00\x00\x00',
    'SO_LINGER': b'\x80\x00\x00\x00',
    'SO_OOBINLINE': b'\x00\x01\x00\x00',
    'SO_REUSEPORT': b'\x00\x02\x00\x00',
    'SO_BLOCKMODE': b'\x00\x10\x00\x00',

    'SO_SNDBUF': b'\x01\x10\x00\x00',
    'SO_SNDTIMEO': b'\x05\x10\x00\x00',
    'SO_RCVTIMEO': b'\x06\x10\x00\x00',
    'SO_ERROR': b'\x07\x10\x00\x00',
    'SO_TYPE': b'\x08\x10\x00\x00',
    'SO_NO_CHECK': b'\x0a\x10\x00\x00'
}

response_header = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Set option for a socket.')

        self.widget.addArg('SockFd', QLineEdit(), '[int] File descriptor for the socket.')

        self.widget.addArg('Level', QComboBox(), 'Option level.')
        self.widget.getArgWidget('Level').addItems(['SOL_SOCKET', 'IPPROTO_IP', 'IPPROTO_TCP', 'IPPROTO_UDP'])

        self.widget.addArg('Optname', QComboBox(), 'Option name.')
        self.widget.getArgWidget('Optname').addItems(['SO_DEBUG', 'SO_ACCEPTCONN', 
            'SO_REUSEADDR', 'SO_KEEPALIVE', 'SO_DONTROUTE', 'SO_BROADCAST',
            'SO_USELOOPBACK','SO_LINGER', 'SO_OOBINLINE', 'SO_REUSEPORT', 'SO_BLOCKMODE',
            'SO_SNDBUF', 'SO_SNDTIMEO', 'SO_RCVTIMEO', 'SO_ERROR', 'SO_TYPE', 'SO_NO_CHECK'
        ])

        self.widget.addArg('Optval', QLineEdit(), '[hex, little] Option value.')

        return self.widget

    def encode(self):
        command = cmdTable['socket_setsockopt_cmd']

        sock_str = self.widget.getArgWidget('SockFd').text()
        fd_input = int(sock_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + fd_input

        level = self.widget.getArgWidget('Level').currentText()
        level_input = levelDict[level]
        command += b'\x01' + level_input

        optname = self.widget.getArgWidget('Optname').currentText()
        optname_input = optnameDict[optname]
        command += b'\x01' + optname_input

        optval_input = bytes.fromhex(self.widget.getArgWidget('Optval').text())
        command += b'\x02' + len(optval_input).to_bytes(2, 'little') + optval_input

        print(command)
        return command

class Event():

    code = eventTable['socket_setsockopt_event']
    name = 'Event.socket.setsockopt'

    def decode(self, payload):
        if len(payload) == response_header.sizeof():
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        else:
            output = ('ERROR: response format error!\r\n')

        return output
