from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

fmt = Struct(
    'type1' /Int8ub,
    'mode' /BytesInteger(4, swapped=True),
    'type2' /Int8ub,
    'status' /BytesInteger(4, swapped=True)
)

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Wi-Fi status event.')
        return self.widget

    def encode(self):
        return None

    def decode(self, cmd, payload):
        if cmd != eventTable['wifi_status_event']:
            return None

        result = fmt.parse(payload)
        if result.mode == 1:
            if result.status == 0:
                return "Station down"
            elif result.mode == 1:
                return "Station up"
        elif result.mode == 0:
            if result.status == 0:
                return "Softap down"
            elif result.mode == 1:
                return "Softap up"

        return None
