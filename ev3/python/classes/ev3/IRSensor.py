#!/usr/bin/env python3
from ev3dev.ev3 import *

class IRSensor:

    def __init__(self, mode='IR-PROX'):
        self.ir = InfraredSensor()
        self.ir.mode = mode

    def getMode(self):
        return self.ir.mode

    def setMode(self, mode):
        self.ir.mode = mode

    def getValue(self):
        return self.ir.value()

        