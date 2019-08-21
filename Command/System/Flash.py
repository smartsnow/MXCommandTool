from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

flashDict = {'SAVE': b'\x01\x00\x00\x00', 'UNSAVE': b'\x00\x00\x00\x00'}

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Flash Wi-Fi Module.')
        self.widget.addArg('Flash', QComboBox(), 'Wi-Fi Flash: SAVE or UNSAVE')
        self.widget.getArgWidget('Flash').addItems(['SAVE', 'UNSAVE'])
        return self.widget

    def encode(self):
        flashuser = self.widget.getArgWidget('Flash').currentText()
        return cmdTable['system_flash_lock_set_cmd'] + b'\x01' + flashDict[flashuser]
