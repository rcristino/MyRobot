#!/usr/bin/env python3
import _thread
from time import sleep
from classes.mocks.Motor import Motor
from classes.mocks.TouchSensor import TouchSensor
from classes.Comms import CommsServer
from classes.Comms import CommsPublisher
from classes.Comms import Message

class Grabber(Motor):

    MOVE = "move"
    STATE = "state#"
    POSITION = "position#"

    def __init__(self, name, device_portCmd, portCmd=5501, portEvt=5502):
        Motor.__init__(self, name, device_portCmd, False)
        self.name = name
        self.speed = 100
        self.posOpen = 75
        self.posClose = -75
        self.state = "open"

        self.grabCommsServer = CommsServer("grabber_cmd", portCmd)
        self.grabCommsPub = CommsPublisher("grabber_evt", portEvt)

        _thread.start_new_thread(self.grabberCommsWorker, (0.1,))
        _thread.start_new_thread(self.grabberTouchWorker, (0.1,))

    def getState(self):
        return self.state

    def updateState(self, state):
        self.state = state
        msg = Message("grabber", self.state)
        self.grabCommsPub.pubEvt(msg)

    def move(self):
        if(self.getState() is "open"):
            self.updateState("running")
            self.movePosition(self.posClose, self.speed)
            self.waitWhileRunning()
            self.updateState("close")
        else:
            self.updateState("running")
            self.movePosition(self.posOpen, self.speed)
            self.waitWhileRunning()
            self.updateState("open")

    def grabberCommsWorker(self, interval=0.1):
        while(True):
            cmd = self.grabCommsServer.recvCmd()
            if cmd.getName() == "grabber":
                if cmd.getValue() == True and self.getState() == "close":
                    self.move()
                    replyCmd = Message("grabber", True)
                    self.grabCommsServer.sendCmdReply(replyCmd)
                if cmd.getValue() == False and self.getState() == "open":
                    self.move()
                    replyCmd = Message("grabber", False)
                    self.grabCommsServer.sendCmdReply(replyCmd)

    def grabberTouchWorker(self, interval=0.1):
        ts = TouchSensor();
        while(True):
            sleep(interval)
            if(ts.value()):
                self.move()
                msg = Message("grabber_touch", True)
                self.grabCommsPub.pubEvt(msg)

    def __str__(self):
        return "[" + self.name + "] Grabber: " + self.portCmd + " state: " + str(self.state)
