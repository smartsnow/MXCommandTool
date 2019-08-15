# author snowyang

import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui


class UsrFileSystemModel(QFileSystemModel):
    def data(self, index, role):
        data = QFileSystemModel.data(self, index, role)
        if role == QtCore.Qt.DisplayRole and type(data) == str:
            return data.split('.')[0]
        return data


class IconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QtGui.QIcon("folder.png")
        else:
            return QtGui.QIcon("file.png")


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.resize(1200, 600)

        self.setWindowTitle('MX Command Tool Version 1.0 Writen By Snow Yang')

        wl = QHBoxLayout(self)
        split_mainwin = QSplitter()
        wl.addWidget(split_mainwin)

        # Main window
        grpbox_logwin = QGroupBox('Log Window')
        split_mainwin.addWidget(grpbox_logwin)

        grpbox_cmdwin = QGroupBox('Command Window')
        split_mainwin.addWidget(grpbox_cmdwin)

        split_mainwin.setStretchFactor(0, 2)
        split_mainwin.setStretchFactor(1, 1)

        # Log window
        layout_logwin = QVBoxLayout()
        grpbox_logwin.setLayout(layout_logwin)

        self.listLog = QListWidget()
        self.listLog.addItem('Welcome!')
        layout_logwin.addWidget(self.listLog)
        layout_serial = QHBoxLayout()
        layout_logwin.addLayout(layout_serial)

        self.buttonRefreshSerialList = QPushButton(
            QtGui.QIcon("refresh.png"), '')
        layout_serial.addWidget(self.buttonRefreshSerialList)
        self.combox_serial = QComboBox()
        layout_serial.addWidget(self.combox_serial)
        self.buttonOpenSerial = QPushButton(QtGui.QIcon("open.png"), 'Open')
        layout_serial.addWidget(self.buttonOpenSerial)
        layout_serial.addStretch()
        self.buttonSendCommand = QPushButton(QtGui.QIcon("send.png"), 'Send')
        layout_serial.addWidget(self.buttonSendCommand)

        # Command window
        layout_cmdwin = QHBoxLayout()
        grpbox_cmdwin.setLayout(layout_cmdwin)

        spilt_cmdwin = QSplitter()
        layout_cmdwin.addWidget(spilt_cmdwin)

        cmdpath = 'Command'
        self.model = UsrFileSystemModel()
        self.model.setRootPath(cmdpath)
        self.model.setIconProvider(IconProvider())
        self.model.setNameFilters(('*.py',))
        self.model.setNameFilterDisables(False)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(cmdpath))
        for i in range(self.model.columnCount() - 1):
            self.tree.hideColumn(i + 1)
        self.tree.setHeaderHidden(True)
        spilt_cmdwin.addWidget(self.tree)

        self.scrollCmd = QScrollArea()
        self.scrollCmd.setWidgetResizable(True)
        spilt_cmdwin.addWidget(self.scrollCmd)

        spilt_cmdwin.setStretchFactor(0, 2)
        spilt_cmdwin.setStretchFactor(1, 5)
