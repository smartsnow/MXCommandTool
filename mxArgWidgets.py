# author snowyang

from PyQt5.QtWidgets import *


class MxArgsWidget(QWidget):

    def __init__(self, description):
        super().__init__()
        self.vlayout = QVBoxLayout(self)
        self.formlayout = QFormLayout()
        self.vlayout.addLayout(self.formlayout)
        self.formlayout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        self.formlayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.vlayout.addWidget(QLabel('Description'))
        self.textBrowser = QTextBrowser()
        self.textBrowser.setText(description)
        self.vlayout.addWidget(self.textBrowser)
        self.argWidgetDict = {}

    def addArg(self, name, inputWidget, tip):
        inputWidget.setToolTip(tip)
        self.argWidgetDict[name] = inputWidget
        self.formlayout.addRow(name, inputWidget)
        self.textBrowser.append('\n%s:\n%s' % (name, tip))

    def getArgWidget(self, name):
        return self.argWidgetDict[name]
