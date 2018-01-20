#!/usr/bin/env python
import zmq
import pickle
import socket
import json
from classes.Logger import Logger

def commsTerminate():
    zmq.Context().destroy()

class Message():

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def getName(self):
        return self.name

    def getValue(self):
        return self.value


class CommsServer:

    def __init__(self, name="unknown", port=5501):
        self.name = name
        self.localAddress = "tcp://*:" + str(port)
        self.ctx = zmq.Context()
        self.socketRep = self.ctx.socket(zmq.REP)
        self.socketRep.bind(self.localAddress)
        Logger.logInfo("[CommsServer:" + self.name + "] listening on " + self.localAddress)

    def recvCmd(self):
        cmd = self.socketRep.recv_pyobj()
        Logger.logInfo("[recvCmd:" + self.name + "] Name: " + cmd.getName() + " Value: " + str(cmd.getValue()))
        return cmd

    def sendCmdReply(self, cmd):
        Logger.logInfo("[sendCmdReply:" + self.name + "] Name: " + cmd.getName() + " Value: " + str(cmd.getValue()))
        self.socketRep.send_pyobj(cmd)

    def getAddress(self):
        return self.localAddress


class CommsClient:

    def __init__(self, target, name="unknown", port=5501):
        self.name = name
        self.target = "tcp://" + target + ":" + str(port)
        self.ctx = zmq.Context()
        self.socketReq = self.ctx.socket(zmq.REQ)
        self.socketReq.connect(self.target)
        Logger.logInfo("[CommsClient:" + self.name + "] connecting to " + self.target)

    def recvCmdReply(self):
        cmdReply = self.socketReq.recv_pyobj()
        Logger.logInfo("[recvCmdReply:" + self.name + "] Name: " + cmdReply.getName() + " Value: " + str(cmdReply.getValue()))
        return cmdReply

    def sendCmd(self, cmd):
        Logger.logInfo("[sendCmd:" + self.name + "] Name: " + cmd.getName() + " Value: " + str(cmd.getValue()))
        self.socketReq.send_pyobj(cmd)

    def getTarget(self):
        return self.target


class CommsPublisher:

    def __init__(self, name="unknown", port=5601):
        self.name = name
        self.localAddress = "tcp://*:" + str(port)
        self.ctx = zmq.Context()
        self.socketPub = self.ctx.socket(zmq.PUB)
        self.socketPub.bind(self.localAddress)
        Logger.logInfo("[CommsPublisher:" + self.name + "] listening on " + self.localAddress)

    def pubEvt(self, evt):
        Logger.logInfo("[pubEvt:" + self.name + "] Name: " + evt.getName() + " Value: " + str(evt.getValue()))
        self.socketPub.send_pyobj(evt)

    def getAddress(self):
        return self.localAddress


class CommsSubcriber:

    def __init__(self, target, name="unknown", port=5601):
        self.name = name
        self.target = "tcp://" + target + ":" + str(port)
        self.ctx = zmq.Context()
        self.socketSub = self.ctx.socket(zmq.SUB)
        self.socketSub.setsockopt_string(zmq.SUBSCRIBE, '') # no topic or filter using ''
        self.socketSub.connect(self.target)

    def recvEvt(self):
        evt = self.socketSub.recv_pyobj()
        Logger.logInfo("[recvEvt:" + self.name + "] Name: " + evt.getName() + " Value: " + str(evt.getValue()))
        return evt

    def getTarget(self):
        return self.target
