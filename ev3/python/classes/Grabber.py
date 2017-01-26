#!/usr/bin/env python3
from ev3dev.ev3 import *
from classes.Motor import Motor

class Grabber(Motor):

    MOVE = "move"
    STATE = "state#"
    POSITION = "position#"

    def __init__(self, name, port):
        Motor.__init__(self, name, port, False)
        self.speed = 100
        self.posOpen = 75
        self.posClose = -75
        self.state = "open"

    def getState(self):
        return self.state

    def move(self):
        if(self.state is "open"):
            self.state = "running"
            self.movePosition(self.posClose, self.speed)
            self.waitWhileRunning()
            self.state = "close"
        else:
            self.state = "running"
            self.movePosition(self.posOpen, self.speed)
            self.state = "running"
            self.waitWhileRunning()
            self.state = "open"


    def __str__(self):
        return "[" + self.name + "] Grabber: " + self.port + " state: " + str(self.state)
