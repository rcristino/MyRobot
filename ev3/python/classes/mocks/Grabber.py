#!/usr/bin/env python3
import _thread
from time import sleep
from classes.mocks.Motor import Motor
from classes.mocks.TouchSensor import TouchSensor
from classes.Logger import Logger
from classes.Comms import CommsServer
from classes.Comms import CommsPublisher
from classes.Comms import Message

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

        self.grabCommsServer = CommsServer(port)
        self.grabCommsPub = CommsPublisher("grabber")

        _thread.start_new_thread(self.grabberCommsWorker, (0.1,))
        _thread.start_new_thread(self.grabberTouchWorker, (0.1,))
        Logger.logDebug("Grabber ready: " + self.grabCommsServer.getAddress())

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
            msg = self.grabCommsServer.recvMsg()
            if msg.getName() == "grabber":
                if msg.getValue() == True and self.state == "close":
                    self.move()
                    reply = Message("grabber", True)
                    self.grabCommsServer.sendMsg(reply)
                    self.grabCommsPub.sendMsg(reply)
                if msg.getValue() == False and self.state == "open":
                    self.move()
                    reply = Message("grabber", False)
                    self.grabCommsServer.sendMsg(reply)
                    self.grabCommsPub.sendMsg(reply)

    def grabberTouchWorker(self, interval=0.1):
        ts = TouchSensor();
        while(True):
            sleep(interval)
            if(ts.value()):
                self.move()

    def __str__(self):
        return "[" + self.name + "] Grabber: " + self.port + " state: " + str(self.state)
