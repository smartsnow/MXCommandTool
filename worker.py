# author snowyang

import os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from importlib import import_module
from hci import Hci


class Worker(QThread):
    # Signals
    signalCmdWindow = pyqtSignal(QWidget)
    signalSerialComboBox = pyqtSignal(list)

    def __init__(self, mainWindow):
        super(Worker, self).__init__()
        # Main window
        self.mainWindow = mainWindow
        # HCI
        self.hci = Hci(self.onHciEvent)
        # Signals
        self.mainWindow.tree.clicked.connect(self.onTreeClicked)
        self.mainWindow.buttonRefreshSerialList.clicked.connect(
            self.refreshSerialList)
        self.mainWindow.buttonSendCommand.clicked.connect(self.sendCommand)
        self.signalCmdWindow.connect(
            lambda x: self.mainWindow.scrollCmd.setWidget(x))
        self.signalSerialComboBox.connect(self.setSerialComboBoxItems)
        # Command Widgets
        self.cmdObjDict = {}
        self.curCmdName = ''

    def run(self):
        pass

    def onTreeClicked(self, index):
        info = self.mainWindow.model.fileInfo(index)
        if info.isFile():
            relpath = os.path.relpath(info.filePath())
            cmdName = os.path.splitext(relpath)[0].replace(
                '/', '.').replace('\\', '.')
            if cmdName not in self.cmdObjDict:
                self.cmdObjDict[cmdName] = import_module(cmdName).Command()
            self.signalCmdWindow.emit(self.cmdObjDict[cmdName].getWidget())
            self.curCmdName = cmdName

    def refreshSerialList(self):
        portlist = self.hci.slip.portlist()
        self.signalSerialComboBox.emit(portlist)

    def setSerialComboBoxItems(self, portlist):
        self.mainWindow.combox_serial.clear()
        self.mainWindow.combox_serial.addItems(portlist)

    def sendCommand(self):
        args = self.cmdObjDict[self.curCmdName].getArgs()
        self.mainWindow.listLog.addItem(str(args))
        self.mainWindow.listLog.scrollToBottom()

    def onHciEvent(evt, val):
        pass
