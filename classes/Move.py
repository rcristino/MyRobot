#!/usr/bin/env python3
import sys
if('ev3dev' in sys.modules):
    from classes.ev3.Motor import Motor
else:
    from classes.mocks.Motor import Motor
from classes.Comms import CommsServer
from classes.Comms import CommsPublisher
from classes.Comms import Message
import _thread
from time import sleep

class Move(Motor):

    def __init__(self, name, device_port, portCmd=5511, portEvt=5512):
        Motor.__init__(self, name, device_port, True)
        self.name = name
        self.device_port = device_port

        self.moveCommsServer = CommsServer(self.name + "_cmd", portCmd)
        self.moveCommsPub = CommsPublisher(self.name + "_evt", portEvt)
        _thread.start_new_thread(self.moveCommsWorker, (0.1,))

        self.updateState("stop")

    def getName(self):
        return self.name

    def getState(self):
        return self.state

    def updateState(self, state):
        self.state = state
        msg = Message(self.name, self.state)
        self.moveCommsPub.pubEvt(msg)

    def startMove(self, speed):
        self.move(speed)
        self.updateState("move")

    def stopMove(self):
        self.stop()
        self.updateState("stop")

    def moveCommsWorker(self, interval=0.1):
        while(True):
            cmd = self.moveCommsServer.recvCmd()
            if cmd.getName() == self.name:
                if int(cmd.getValue()) != 0 and self.getState() == "stop":
                    self.startMove(int(cmd.getValue()))
                    replyCmd = Message(self.name, True)
                    self.moveCommsServer.sendCmdReply(replyCmd)
                if int(cmd.getValue()) == 0 and self.getState() == "move":
                    self.stopMove()
                    replyCmd = Message(self.name, True)
                    self.moveCommsServer.sendCmdReply(replyCmd)
            else:
                replyCmd = Message(self.name, False)
                self.moveCommsServer.sendCmdReply(replyCmd)

    def __str__(self):
        return "[" + self.name + "] Move: " + self.device_port + " Speed: " + str(self.speed)
