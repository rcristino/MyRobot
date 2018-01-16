#!/usr/bin/env python3
import sys
if('ev3dev' in sys.modules):
    from classes.ev3.IRSensor import IRSensor
else:
    from classes.mocks.IRSensor import IRSensor
from time import sleep
import _thread

from classes.Comms import CommsPublisher
from classes.Comms import Message

class Radar:

    #FIXME to be checked and deleted
    DISTANCE = "dist#"

    def __init__(self, name="radar", rate=0.1, portEvt=5532):
        self.distance = 0
        self.name = name
        self.ir = IRSensor('IR-PROX')
        _thread.start_new_thread(self.radarWorker, (rate, ))
        
        self.radarCommsPub = CommsPublisher(self.name + "_evt", portEvt)

    def getName(self):
        return self.name

    def getDistance(self):
        return self.distance

    def radarWorker(self, rate):
        while True:
            self.distance = self.ir.getValue()
            msg = Message(self.name, self.distance)
            self.radarCommsPub.pubEvt(msg)
            sleep(rate)
