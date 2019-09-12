from mxArgWidgets import *
from cmdTable import cmdTable, eventTable

domainDict = {'AF_INET': b'\x02\x00\x00\x00', 'AF_INET6': b'\x0a\x00\x00\x00'}
typeDict = {'SOCK_STREAM': b'\x01\x00\x00\x00', 'SOCK_DGRAM': b'\x02\x00\x00\x00'}
protocolDict = {'IPPROTO_TCP': b'\x06\x00\x00\x00', 'IPPROTO_UDP': b'\x11\x00\x00\x00'}

class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Create a socket.')

        self.widget.addArg('Domain', QComboBox(), 'Domain of the socket.')
        self.widget.getArgWidget('Domain').addItems(['AF_INET', 'AF_INET6'])

        self.widget.addArg('Type', QComboBox(), 'Type of the socket.')
        self.widget.getArgWidget('Type').addItems(['SOCK_STREAM', 'SOCK_DGRAM'])

        self.widget.addArg('Protocol', QComboBox(), 'Protocol of the socket.')
        self.widget.getArgWidget('Protocol').addItems(['IPPROTO_TCP', 'IPPROTO_UDP'])

        return self.widget

    def encode(self):
        command = cmdTable['socket_create_cmd']

        domain = self.widget.getArgWidget('Domain').currentText()
        command += b'\x01' +  domainDict[domain]

        type = self.widget.getArgWidget('Type').currentText()
        command += b'\x01' +  typeDict[type]

        protocol = self.widget.getArgWidget('Protocol').currentText()
        command += b'\x01' +  protocolDict[protocol]

        print(command)
        return command
