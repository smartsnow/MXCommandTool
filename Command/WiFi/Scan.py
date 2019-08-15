from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Scan Access-Points around us.')
        return self.widget

    def getArgs(self):
        return None

    def parse(self, data):
        pass
