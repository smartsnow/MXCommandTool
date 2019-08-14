from PyQt5.QtWidgets import *

description = '''
You can prevent people (other than the super-user) from writing to you
with the mesg(1) command.

If the user you want to write to is logged in on more than one terminal,
you can specify which terminal to write to by specifying the terminal
name as the second operand to the write command.  Alternatively, you can
let write select one of the terminals - it will pick the one with the
shortest idle time.  This is so that if the user is logged in at work and
also dialed up from home, the message will go to the right place.

The traditional protocol for writing to someone is that the string `-o',
either at the end of a line or on a line by itself, means that it's the
other person's turn to talk.  The string `oo' means that the person
believes the conversation to be over.
'''

class Command():

    def __init__(self):
        self.widget = QWidget()
        formlayout = QFormLayout(self.widget)
        formlayout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        formlayout.addRow('FD', QLineEdit())
        formlayout.addRow('Data', QTextEdit())
        textBrowser = QTextBrowser()
        textBrowser.setText(description)
        formlayout.addRow('Description', textBrowser)

    def getWidget(self):
        return self.widget

    def getArgs(self):
        pass

    def parse(self, data):
        pass
