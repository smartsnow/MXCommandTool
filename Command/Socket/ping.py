from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

response_header = Struct(
    'type' /Int8ub,
    'ret' /BytesInteger(4, signed=True, swapped=True)
)

response_data = Struct(
    'type_resp' /Int8ub,
    'len_resp' /BytesInteger(2, signed=False, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Ping a host name.')

        self.widget.addArg('Hostname', QLineEdit(), '[string] Hostname or IPv4 address in standard dot notation.')
        self.widget.addArg('Count', QLineEdit(), '[int] maximum ping counts.')
        self.widget.addArg('Delay', QLineEdit(), '[int] maximum delay in millisecond.')

        return self.widget

    def encode(self):
        command = cmdTable['socket_ping_cmd']

        hostname_str = self.widget.getArgWidget('Hostname').text().encode()
        command += b'\x02' + len(hostname_str).to_bytes(2, 'little') + hostname_str

        count_str = self.widget.getArgWidget('Count').text()
        count_input = int(count_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + count_input

        delay_str = self.widget.getArgWidget('Delay').text()
        delay_input = int(delay_str, base=10).to_bytes(4, 'little')
        command += b'\x01' + delay_input

        print(command)
        return command

class Event():

    code = eventTable['socket_ping_event']
    name = 'Event.socket.ping'

    def decode(self, payload):
        if len(payload) == response_header.sizeof():
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
        elif len(payload) >= (response_header.sizeof() + response_data.sizeof()):
            result = response_header.parse(payload)
            output = ('return: %d\r\n' % (result.ret))
            if result.ret < 0:
                return output
            else:
                index = response_header.sizeof()
                data = response_data.parse(payload[index:])
                index += response_data.sizeof()
                count = int((data.len_resp / 4))
                output += ('count: %d\r\n' % count)
                for i in range(0, count):
                    delay_ms = int.from_bytes(payload[index:index+4], byteorder='little', signed=False)
                    output += ( '\tseq=%d\ttime=%d ms\r\n' % (i + 1, delay_ms) )
                    index += 4
        else:
            output = ('ERROR: response format error!\r\n')

        return output
