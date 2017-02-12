#!/usr/bin/env python3
from ev3dev.ev3 import *
import zmq
import socket
import _thread
from time import sleep
from classes.Motor import Motor
from classes.Logger import Logger

class Grabber(Motor):

    MOVE = "move"
    STATE = "state#"
    POSITION = "position#"

    def __init__(self, name, device_port, port=5501):
        Motor.__init__(self, name, device_port, False)
        self.name = name
        self.speed = 100
        self.posOpen = 75
        self.posClose = -75
        self.state = "open"
        self.localAddress = "tcp://*:" + str(port)
        self.ctx = zmq.Context()
        self.socketRep = self.ctx.socket(zmq.REP)
        self.socketRep.bind(self.localAddress)
        _thread.start_new_thread(self.grabberCommsWorker, (0.1,))
        _thread.start_new_thread(self.grabberTouchWorker, (0.1,))
        Logger.logDebug("Grabber ready: " + self.localAddress)

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

    def grabberCommsWorker(self, interval=0.1):
        while(True):
            sleep(interval)
            data = self.socketRep.recv_string()
            if data.find(Grabber.MOVE) is not -1:
                self.move()
                self.socketRep.send_string("True")
            else:
                self.socketRep.send_string("False")

    def grabberTouchWorker(self, interval=0.1):
        ts = TouchSensor();
        while(True):
            sleep(interval)
            if(ts.value()):
                self.move()

    def __str__(self):
        return "[" + self.name + "] Grabber: " + self.port + " state: " + str(self.state)
