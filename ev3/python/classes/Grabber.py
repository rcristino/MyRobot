#!/usr/bin/env python3
from ev3dev.ev3 import *
from classes.Motor import Motor

class Grabber(Motor):

    OPEN = "open"
    CLOSE = "close"
    STATE = "state#"
    POSITION = "position#"

    def __init__(self, name, port):
        Motor.__init__(self, name, port, False)
        self.speed = 100
        self.posOpen = 75
        self.posClose = -75
        self.state = Grabber.OPEN

    def getState(self):
        return self.state

    def open(self):
        if(self.state is Grabber.CLOSE):
            self.movePosition(self.posOpen, self.speed)
            self.state = Grabber.OPEN
            self.wait()

    def close(self):
        if(self.state is Grabber.OPEN):
            self.movePosition(self.posClose, self.speed)
            self.state = Grabber.CLOSE
            self.wait()


    def __str__(self):
        return "[" + self.name + "] Grabber: " + self.port + " State: " + str(self.state)
