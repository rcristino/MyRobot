#!/usr/bin/env python
import zmq
import pickle
import socket
import json

class Message():

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def getName(self):
        return self.name

    def getValue(self):
        return self.value


class CommsServer:

    def __init__(self, port=5501):
        self.localAddress = "tcp://*:" + str(port)
        self.ctx = zmq.Context()
        self.socketRep = self.ctx.socket(zmq.REP)
        self.socketRep.bind(self.localAddress)

    def recvCmd(self):
        return self.socketRep.recv_pyobj()

    def sendCmdReply(self, obj):
        self.socketRep.send_pyobj(obj)

    def getAddress(self):
        return self.localAddress


class CommsClient:

    def __init__(self, target, port=5501):
        self.target = "tcp://" + target + ":" + str(port)
        self.ctx = zmq.Context()
        self.socketReq = self.ctx.socket(zmq.REQ)
        self.socketReq.connect(self.target)

    def recvCmdReply(self):
        return self.socketReq.recv_pyobj()

    def sendCmd(self, obj):
        self.socketReq.send_pyobj(obj)

    def getTarget(self):
        return self.target


class CommsPublisher:

    def __init__(self, port=5601):
        self.localAddress = "tcp://*:" + str(port)
        self.ctx = zmq.Context()
        self.socketPub = self.ctx.socket(zmq.PUB)
        self.socketPub.bind(self.localAddress)

    def pubEvt(self, obj):
        self.socketPub.send_pyobj(obj)

    def getAddress(self):
        return self.localAddress


class CommsSubcriber:

    def __init__(self, target, port=5601):
        self.target = "tcp://" + target + ":" + str(port)
        self.ctx = zmq.Context()
        self.socketSub = self.ctx.socket(zmq.SUB)
        self.socketSub.setsockopt_string(zmq.SUBSCRIBE, '') # no topic or filter using ''
        self.socketSub.connect(self.target)

    def recvEvt(self):
        evt = self.socketSub.recv_pyobj()
        return evt

    def getTarget(self):
        return self.target
