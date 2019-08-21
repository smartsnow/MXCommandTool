from mxArgWidgets import *
from cmdTable import cmdTable, eventTable
from construct import *

fmt = Struct(
    'type1' /Int8ub,
    'mode' /BytesInteger(4, swapped=True),
    'type2' /Int8ub,
    'status' /BytesInteger(4, swapped=True)
)

class Event():

    code = eventTable['wifi_status_event']
    name = 'Wi-Fi status'

    def decode(self, payload):
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
