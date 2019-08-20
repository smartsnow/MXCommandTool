from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget("Get Wi-Fi module's version.")
        self.widget.addArg('Data', MxHexStrEdit(), 'Echo data.')
        return self.widget

    def encode(self):
        userinput = self.widget.getArgWidget('Data').text().encode()
        length = len(userinput)
        command = cmdTable['ipc_echo_cmd'] + b'\x02' + length.to_bytes(2, 'little') + userinput
        return command

    def decode(self, cmd, payload):
        if cmd != eventTable['ipc_echo_event']:
            return None
        return payload[3:].decode()
