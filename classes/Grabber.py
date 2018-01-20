#!/usr/bin/env python3
import sys
if('ev3dev' in sys.modules):
    from classes.ev3.Motor import Motor
    from classes.ev3.Touch import Touch
else:
    from classes.mocks.Motor import Motor
    from classes.mocks.Touch import Touch
from classes.Comms import CommsServer
from classes.Comms import CommsPublisher
from classes.Comms import Message
import _thread
from time import sleep

class Grabber(Motor):

    #FIXME to be checked and deleted
    MOVE = "move"
    STATE = "state#"
    POSITION = "position#"

    def __init__(self, name, device_port, portCmd=5501, portEvt=5502):
        Motor.__init__(self, name, device_port, False)
        self.name = name
        self.speed = 100
        self.posOpen = 75
        self.posClose = -75

        self.grabCommsServer = CommsServer(self.name + "_cmd", portCmd)
        self.grabCommsPub = CommsPublisher(self.name + "_evt", portEvt)
        _thread.start_new_thread(self.grabberCommsWorker, (0.1,))
        _thread.start_new_thread(self.grabberTouchWorker, (0.1,))

        self.updateState("open")
        
    def getState(self):
        return self.state

    def updateState(self, state):
        self.state = state
        msg = Message(self.name, self.state)
        self.grabCommsPub.pubEvt(msg)

    def grabberMove(self):
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
            if cmd.getName() == self.name:
                if cmd.getValue() == True and self.getState() == "close":
                    self.grabberMove()
                    replyCmd = Message(self.name, True)
                    self.grabCommsServer.sendCmdReply(replyCmd)
                if cmd.getValue() == False and self.getState() == "open":
                    self.grabberMove()
                    replyCmd = Message(self.name, True)
                    self.grabCommsServer.sendCmdReply(replyCmd)
            else:
                replyCmd = Message(self.name, False)
                self.grabCommsServer.sendCmdReply(replyCmd)

    def grabberTouchWorker(self, interval=0.1):
        ts = TouchSensor();
        while(True):
            sleep(interval)
            if(ts.value()):
                self.grabberMove()
                msg = Message("grabber_touch", True)
                self.grabCommsPub.pubEvt(msg)

    def __str__(self):
        return "[" + self.name + "] Grabber: " + self.portCmd + " state: " + str(self.state)
