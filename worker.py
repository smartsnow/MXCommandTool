# author snowyang

import os
import time
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from importlib import import_module
from hci import Hci
from argsJson import ArgsJson

class Worker(QThread):
    # Signals
    signalLogTableAddRow = pyqtSignal(list)
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
        self.mainWindow.buttonClearLogWindow.clicked.connect(self.clearLogWindow)
        self.signalLogTableAddRow.connect(self.addLogListItem)
        self.signalSerialException.connect(self.SerialExceptionHandler)
        # Command Widgets
        self.cmdObjDict = {}
        self.curCmdName = ''
        self.refreshSerialList()
        self.argsJson = ArgsJson()

    def run(self):
        while True:
            data = self.hci.read()
            cmd = data[:2]
            payload = data[2:]
            for cmdName in self.cmdObjDict:
                formatOutput = self.cmdObjDict[cmdName].decode(cmd, payload)
                if not formatOutput:
                    continue
                self.signalLogTableAddRow.emit([time.strftime("%T"), cmdName, formatOutput])
                break

    def onTreeClicked(self, index):
        info = self.mainWindow.model.fileInfo(index)
        if info.isFile():
            relpath = os.path.relpath(info.filePath())
            cmdName = os.path.splitext(relpath)[0].replace(
                '/', '.').replace('\\', '.')
            if cmdName not in self.cmdObjDict:
                self.cmdObjDict[cmdName] = import_module(cmdName).Command()
            if self.curCmdName:
                self.saveRecordFromArgsWidget(self.curCmdName, self.mainWindow.scrollCmd.widget())
            self.mainWindow.scrollCmd.setWidget(self.cmdObjDict[cmdName].getWidget())
            if cmdName in self.argsJson.argsDict:
                self.loadRecordToArgsWidget(cmdName, self.mainWindow.scrollCmd.widget())
            self.curCmdName = cmdName
            self.argsJson.argsDict['curCmdName'] = cmdName

    def saveRecordFromArgsWidget(self, name, widget):
        curDict = {}
        for argName in widget.argWidgetDict:
            argWidget = widget.argWidgetDict[argName]
            if type(argWidget) == QLineEdit:
                curDict[argName] = argWidget.text()
        self.argsJson.argsDict[name] = curDict

    def loadRecordToArgsWidget(self, name, widget):
        curDict = self.argsJson.argsDict[name]
        for argName in widget.argWidgetDict:
            argWidget = widget.argWidgetDict[argName]
            if type(argWidget) == QLineEdit:
                argWidget.setText(curDict[argName])

    def clearLogWindow(self):
        self.mainWindow.logTable.setRowCount(0)

    def refreshSerialList(self):
        portlist = self.hci.slip.portlist()
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

