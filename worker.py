import os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from importlib import import_module
from hci import Hci


class Worker(QThread):
    # Signals
    signalArgsWindow = pyqtSignal(QWidget)
    signalSerialComboBox = pyqtSignal(list)

    def __init__(self, mainWindow):
        super(Worker, self).__init__()
        # Main window
        self.mainWindow = mainWindow
        # HCI
        self.hci = Hci(self.onHciEvent)
        # Signals
        self.mainWindow.tree.clicked.connect(self.onTreeClicked)
        self.signalArgsWindow.connect(
            lambda x: self.mainWindow.scroll_args.setWidget(x))
        self.mainWindow.buttonRefreshSerialList.clicked.connect(
            self.refreshSerialList)
        self.signalSerialComboBox.connect(self.setSerialComboBoxItems)

    def run(self):
        pass

    def onTreeClicked(self, index):
        info = self.mainWindow.model.fileInfo(index)
        if info.isFile():
            relpath = os.path.relpath(info.filePath())
            modpath = os.path.splitext(relpath)[0].replace(
                '/', '.').replace('\\', '.')
            module = import_module(modpath)
            cmdobj = module.Command()
            self.signalArgsWindow.emit(cmdobj.widget)

    def refreshSerialList(self):
        portlist = self.hci.slip.portlist()
        self.signalSerialComboBox.emit(portlist)

    def setSerialComboBoxItems(self, portlist):
        self.mainWindow.combox_serial.clear()
        self.mainWindow.combox_serial.addItems(portlist)

    def onHciEvent(evt, val):
        pass
