from PyQt5.QtWidgets import *


class Command():

    def __init__(self):
        self.widget = QWidget()
        formlayout = QFormLayout(self.widget)
        formlayout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        formlayout.addRow('SSID', QLineEdit())
        formlayout.addRow('Passphrase', QLineEdit())
        textBrowser = QTextBrowser()
        textBrowser.setText('Connect to an Acess-Point')
        formlayout.addRow('Description', textBrowser)

    def getArgs(self):
        pass

    def parse(self, data):
        pass
