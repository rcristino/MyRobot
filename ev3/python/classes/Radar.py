#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import _thread

class Radar:

    DISTANCE = "dist#"

    def __init__(self, rate=0.1):
        self.ir = InfraredSensor()
        self.ir.mode = 'IR-PROX'
        _thread.start_new_thread(self.radarWorker, (rate, ))
        self.distance = 0

    def getDistance(self):
        return self.distance

    def radarWorker(self, rate):

        while True:
            self.distance = self.ir.value()
            sleep(rate)
