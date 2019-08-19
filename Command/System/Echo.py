from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget("Get Wi-Fi module's version.")
        self.widget.addArg('Data', MxHexStrEdit(), 'Echo data.')
        return self.widget

    def encode(self):
        userinput = self.widget.getArgWidget('Data').text().encode()
        length = len(userinput)
        command = b'\x01\x10' + b'\x02' + length.to_bytes(2, 'little') + userinput
        return command

    def decode(self, cmd, payload):
        if cmd != b'\x01\x20':
            return None
        return payload[3:].decode()
