#!/usr/bin/env python3
from random import *

class IRSensor:

    def __init__(self, mode='IR-PROX'):
        self.mode = mode
        print("IR INIT MODE=" + self.mode)

    def getMode(self):
        return self.mode

    def setMode(self, mode):
        print("IR NEW MODE=" + self.mode)
        self.mode = mode

    def getValue(self):
        return randint(1, 50)

        