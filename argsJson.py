import os
import json


class ArgsJson():

    def __init__(self):
        self.argsJsonFileName = 'args.json'
        self.argsDict = {}
        if not os.path.exists(self.argsJsonFileName):
            json.dump(self.argsDict, open(self.argsJsonFileName, 'w'))
        else:
            self.argsDict = json.load(open(self.argsJsonFileName, 'r'))

    def save(self):
        json.dump(self.argsDict, open(self.argsJsonFileName, 'w'))
