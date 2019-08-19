# author snowyang

import os
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

longDescription = '''Version\t: 1.0.0
Author\t: Snow Yang
Bug Reports\t: yangsw@mxchip.com'''

groupBoxStyleSheet = \
    '''
QGroupBox::title 
{
    subcontrol-position: top center; 
}
'''

class UsrFileSystemModel(QFileSystemModel):
    def data(self, index, role):
        data = QFileSystemModel.data(self, index, role)
        if role == QtCore.Qt.DisplayRole and type(data) == str:
            return data.split('.')[0]
        return data


class IconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QtGui.QIcon("resources/folder.png")
        else:
            return QtGui.QIcon("resources/file.png")


class LogTableWidget(QTableWidget):

    def __init__(self):
        super().__init__()
        headerLabels = ['Time', 'Command', 'Value']
        self.setColumnCount(len(headerLabels))
        self.setHorizontalHeaderLabels(headerLabels)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)

    def addRow(self, rowItems):
        rowPosition = self.rowCount()
        self.insertRow(rowPosition)
        for i in range(self.columnCount()):
            self.setItem(rowPosition, i, QTableWidgetItem(rowItems[i]))
        self.resizeRowToContents(rowPosition)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1200, 600)
        self.setWindowTitle('MX Command Tool')

        wl = QHBoxLayout(self)
        split_mainwin = QSplitter()
        wl.addWidget(split_mainwin)

        # Main window
        grpbox_logwin = QGroupBox('Log Window')
        grpbox_logwin.setStyleSheet(groupBoxStyleSheet)
        split_mainwin.addWidget(grpbox_logwin)

        grpbox_cmdwin = QGroupBox('Command Window')
        grpbox_cmdwin.setStyleSheet(groupBoxStyleSheet)
        split_mainwin.addWidget(grpbox_cmdwin)

        split_mainwin.setStretchFactor(0, 2)
        split_mainwin.setStretchFactor(1, 1)

        # Log window
        layout_logwin = QVBoxLayout()
        grpbox_logwin.setLayout(layout_logwin)

        self.logTable = LogTableWidget()
        self.logTable.addRow([time.strftime("%T"), '', longDescription])
        self.logTable.resizeColumnsToContents()
        layout_logwin.addWidget(self.logTable)
        layout_serial = QHBoxLayout()
        layout_logwin.addLayout(layout_serial)

        self.buttonRefreshSerialList = QPushButton(
            QtGui.QIcon("resources/refresh.png"), '')
        self.buttonRefreshSerialList.setToolTip('Refresh Serial List')
        layout_serial.addWidget(self.buttonRefreshSerialList)
        self.combox_serial = QComboBox()
        layout_serial.addWidget(self.combox_serial)
        self.buttonOpenCloseSerial = QPushButton(
            QtGui.QIcon("resources/closed.png"), '')
        self.buttonOpenCloseSerial.setToolTip('Open Serial')
        layout_serial.addWidget(self.buttonOpenCloseSerial)
        self.buttonClearLogWindow = QPushButton(
            QtGui.QIcon("resources/clear.png"), '')
        self.buttonClearLogWindow.setToolTip('Clear Log Window')
        layout_serial.addWidget(self.buttonClearLogWindow)
        layout_serial.addStretch()
        self.buttonSendCommand = QPushButton(
            QtGui.QIcon("resources/send.png"), '')
        self.buttonSendCommand.setToolTip('Send Command')
        self.buttonSendCommand.setEnabled(False)
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
        self.tree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tree.setMinimumWidth(180)
        spilt_cmdwin.addWidget(self.tree)

        self.scrollCmd = QScrollArea()
        self.scrollCmd.setWidgetResizable(True)
        spilt_cmdwin.addWidget(self.scrollCmd)

        spilt_cmdwin.setStretchFactor(0, 2)
        spilt_cmdwin.setStretchFactor(1, 5)
