from PyQt5.QtWidgets import *


class Command():

    def __init__(self):
        self.widget = QWidget()
        formlayout = QFormLayout(self.widget)
        formlayout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        textBrowser = QTextBrowser()
        textBrowser.setText('Disconnect from Access-Point')
        formlayout.addRow('Description', textBrowser)

    def getWidget(self):
        return self.widget

    def getArgs(self):
        pass

    def parse(self, data):
        pass
