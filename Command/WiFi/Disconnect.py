from mxArgWidgets import *


class Command():

    def getWidget(self):
        self.widget = MxArgsWidget('Disconnect from an Acess-Point.')
        return self.widget

    def getArgs(self):
        return None

    def parse(self, data):
        pass
