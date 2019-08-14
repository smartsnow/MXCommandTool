#!/usr/bin/env python3
# author snowyang

import os
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import importlib
import hci


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


fuckyou = '''
                   .::::.
                 .::::::::.
                :::::::::::  FUCK YOU
            ..:::::::::::'
          '::::::::::::'
            .::::::::::
       '::::::::::::::..
            ..::::::::::::.
            ::::::::::::::::
           ::::  :::::::::'        .:::.
          ::::'   ':::::'       .::::::::.
        .::::'      ::::     .:::::::'::::.
       .:::'       :::::  .:::::::::' ':::::.
      .::'        :::::.:::::::::'      ':::::.
     .::'         ::::::::::::::'           ::::.
 ...:::           ::::::::::::'                ::.
     ':.          ':::::::::'                  ::::..
                   '.:::::'                    ':'   ..
'''


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()
        self.setWindowTitle('MX Command Tool Version 1.0 Writen By Snow Yang')
        self.resize(1200, 600)

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

        list_log = QListWidget()
        list_log.addItem('Welcome!')
        list_log.addItem(fuckyou)
        layout_logwin.addWidget(list_log)
        layout_serial = QHBoxLayout()
        layout_logwin.addLayout(layout_serial)

        self.buttonRefreshSerialList = QPushButton(
            QtGui.QIcon("refresh.png"), 'Refresh')
        self.buttonRefreshSerialList.clicked.connect(self.refreshSerialList)
        layout_serial.addWidget(self.buttonRefreshSerialList)
        self.combox_serial = QComboBox()
        self.combox_serial.SizeAdjustPolicy(QComboBox.AdjustToContents)
        layout_serial.addWidget(self.combox_serial)
        layout_serial.addWidget(QPushButton(QtGui.QIcon("open.png"), 'Open'))
        layout_serial.addStretch()
        layout_serial.addWidget(QPushButton(QtGui.QIcon("send.png"), 'Send'))

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
        self.tree.clicked.connect(self.onTreeClicked)

        self.scroll_args = QScrollArea()
        spilt_cmdwin.addWidget(self.scroll_args)

        spilt_cmdwin.setStretchFactor(0, 2)
        spilt_cmdwin.setStretchFactor(1, 5)

        def on_event(evt, val):
            if evt == 'resume':
                print('[Event][Comport resumed] port=%d' % val)
            elif evt == 'close':
                print('[Error][Comport closed] reason=%d' % val)
            elif evt == 'lost':
                print('[Error][Sent data failed] seq=%d' % val)
            elif evt == 'timeout':
                print('[Warning][Send data timeout] seq=%d, retry=%d' %
                      (val[0], val[1]))
            elif evt == 'crcerror':
                print('[Warning][Frame CRC error] type=%d, seq=%d, crc=%d, crccal=%d' % (
                    val[0], val[1], val[2], val[3]))
            elif evt == 'ackoos':
                print('[Warning][ACK Out Of Sequence] seq=%d' % val)

        self.hci = hci.Hci(on_event)

    def refreshSerialList(self):
        portlist = self.hci.slip.portlist()
        self.combox_serial.clear()
        self.combox_serial.addItems(portlist)

    def onTreeClicked(self, index):
        info = self.model.fileInfo(index)
        if info.isFile():
            relpath = os.path.relpath(info.filePath())
            modpath = os.path.splitext(relpath)[0].replace(
                '/', '.').replace('\\', '.')
            module = importlib.import_module(modpath)
            cmdobj = module.Command()
            self.scroll_args.setWidget(cmdobj.widget)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    font = QtGui.QFont("Calibri")
    app.setFont(font)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # app.setStyleSheet(open('style.css').read())
    win.show()
    sys.exit(app.exec_())
