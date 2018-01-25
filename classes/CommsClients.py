#!/usr/bin/env python
import _thread
from time import sleep
from classes.Comms import CommsClient
from classes.Comms import CommsSubcriber
from classes.Comms import Message

class CommsClientRobot:
    def __init__(self, name, target, portCmd=5000):
        self.target = target
        self.name = name
        self.mainCommsClient = CommsClient(self.target, "test_robot_cmd", portCmd)

    def action(self, act="shutdown"):
        cmd = Message(self.name, act)
        self.mainCommsClient.sendCmd(cmd)
        self.reply = self.mainCommsClient.recvCmdReply()

    def getReply(self):
        return self.reply


class CommsClientMove:
    def __init__(self, name, target, portCmd=5511, portEvt=5512):
        self.target = target
        self.name = name
        self.moveCommsClient = CommsClient(self.target, "test_move_cmd", portCmd)
        self.moveCommsSub = CommsSubcriber(self.target, "test_move_evt", portEvt)
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def getReply(self):
        return self.reply

    def getEvent(self):
        return self.evt

    def action(self, speed):
        cmd = Message(self.name, speed)
        self.moveCommsClient.sendCmd(cmd)
        self.reply = self.moveCommsClient.recvCmdReply()

    def workerStatus(self, interval=0.1):
        while True:
            self.evt = self.moveCommsSub.recvEvt()


class CommsClientGrabber:
    def __init__(self, target, portCmd=5501, portEvt=5502):
        self.target = target
        self.name = "grabber"
        self.grabCommsClient = CommsClient(self.target, "test_grabber_cmd", portCmd)
        self.grabCommsSub = CommsSubcriber(self.target, "test_grabber_evt", portEvt)
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def getReply(self):
        return self.reply

    def getEvent(self):
        return self.evt

    def action(self, toOpen):
        cmd = Message(self.name,toOpen)
        self.grabCommsClient.sendCmd(cmd)
        self.reply = self.grabCommsClient.recvCmdReply()

    def workerStatus(self, interval=0.1):
        while True:
            self.evt = self.grabCommsSub.recvEvt()


class CommsClientRadar:
    def __init__(self, name, target, portEvt=5532):
        self.target = target
        self.name = name
        self.radarCommsSub = CommsSubcriber(self.target, "test_radar_evt", portEvt)
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def getEvent(self):
        return self.evt

    def workerStatus(self, interval=0.1):
        while True:
            self.evt = self.radarCommsSub.recvEvt()

