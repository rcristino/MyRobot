#!/usr/bin/env python3

class IRSensor:

    def __init__(self, mode='IR-PROX', rate=0.1):
        self.mode = mode
        print("IR INIT MODE=" + self.mode)

    def getMode(self):
        return self.mode

    def setMode(self, mode):
        print("IR NEW MODE=" + self.mode)
        self.mode = mode

    def getValue(self):
        return 10

        