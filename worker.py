# author snowyang

import os
import time
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from importlib import import_module
from hci import Hci


class Worker(QThread):
    # Signals
    signalCmdWindow = pyqtSignal(QWidget)
    signalSerialComboBox = pyqtSignal(list)
    signalLogList = pyqtSignal(list)
    signalSerialException = pyqtSignal(str)

    def __init__(self, mainWindow):
        super(Worker, self).__init__()
        # Main window
        self.mainWindow = mainWindow
        # HCI
        self.hci = Hci(self.onHciEvent)
        # Signals
        self.mainWindow.tree.clicked.connect(self.onTreeClicked)
        self.mainWindow.buttonRefreshSerialList.clicked.connect(self.refreshSerialList)
        self.mainWindow.buttonSendCommand.clicked.connect(self.sendCommand)
        self.mainWindow.buttonOpenCloseSerial.clicked.connect(self.openCloseSerial)
        self.signalCmdWindow.connect(lambda x: self.mainWindow.scrollCmd.setWidget(x))
        self.signalSerialComboBox.connect(self.setSerialComboBoxItems)
        self.signalLogList.connect(self.addLogListItem)
        self.signalSerialException.connect(self.SerialExceptionHandler)
        # Command Widgets
        self.cmdObjDict = {}
        self.curCmdName = ''

    def run(self):
        self.refreshSerialList()
        while True:
            data = self.hci.read()
            cmd = data[:2]
            payload = data[2:]
            for cmdName in self.cmdObjDict:
                formatOutput = self.cmdObjDict[cmdName].decode(cmd, payload)
                if not formatOutput:
                    continue
                self.signalLogList.emit([time.strftime("%T"), cmdName, formatOutput])
                break

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
        if self.curCmdName == '':
            return
        args = self.cmdObjDict[self.curCmdName].encode()
        self.hci.write(args)

    def openCloseSerial(self):
        if self.mainWindow.buttonOpenCloseSerial.toolTip() == 'Open Serial':
            try:
                self.hci.open(self.mainWindow.combox_serial.currentText())
            except Exception as e:
                QMessageBox.warning(self.mainWindow, '', 'Open Serial Failed!\n\n%s' % (e), QMessageBox.Yes, QMessageBox.Yes)
                return
            self.mainWindow.buttonOpenCloseSerial.setIcon(QIcon("resources/opened.png"))
            self.mainWindow.buttonOpenCloseSerial.setToolTip('Close Serial')
            self.mainWindow.buttonSendCommand.setEnabled(True)
        else:
            self.hci.close()
            self.mainWindow.buttonOpenCloseSerial.setIcon(QIcon("resources/closed.png"))
            self.mainWindow.buttonOpenCloseSerial.setToolTip('Open Serial')
            self.mainWindow.buttonSendCommand.setEnabled(False)

    def addLogListItem(self, rowItems):
        self.mainWindow.logTable.addRow(rowItems)
        self.mainWindow.logTable.scrollToBottom()

    def SerialExceptionHandler(self, text):
        QMessageBox.warning(self.mainWindow, '', text, QMessageBox.Yes, QMessageBox.Yes)
        self.mainWindow.buttonOpenCloseSerial.setIcon(QIcon("resources/closed.png"))
        self.mainWindow.buttonOpenCloseSerial.setToolTip('Open Serial')
        self.mainWindow.buttonSendCommand.setEnabled(False)
        self.refreshSerialList()

    def onHciEvent(self, evt, val):
        print('event=%s, value=%s' % (evt, val))
        if evt == 'serial':
            self.signalSerialException.emit('Serial Exception!\n\n%s' % (val))

