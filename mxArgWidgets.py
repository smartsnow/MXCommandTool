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
        self.textBrowser.setMinimumHeight(300)
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


class MxHexStrEdit(QWidget):

    def __init__(self):
        super().__init__()
        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        self.buttonToggle = QPushButton('Convert to HEX')
        vlayout.addWidget(self.buttonToggle)
        self.plainTextEdit = QPlainTextEdit()
        vlayout.addWidget(self.plainTextEdit)
        self.buttonToggle.clicked.connect(self.toggleFormat)

    def toggleFormat(self):
        if self.buttonToggle.text() == 'Convert to HEX':
            self.buttonToggle.setText('Convert to STRING')
            strText = self.plainTextEdit.toPlainText()
            hexText = strText.encode().hex().upper()
            self.plainTextEdit.setPlainText(hexText)
        else:
            hexText = self.plainTextEdit.toPlainText()
            try:
                strText = bytes.fromhex(hexText).decode()
            except Exception as e:
                QMessageBox.warning(self, '', 'Invalid HEX Format!\n\n%s'%(e), QMessageBox.Yes, QMessageBox.Yes)
                return
            self.plainTextEdit.setPlainText(strText)
            self.buttonToggle.setText('Convert to HEX')

    def text(self):
        return self.plainTextEdit.toPlainText()
