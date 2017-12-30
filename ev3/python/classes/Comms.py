#!/usr/bin/env python
import zmq
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

    def recvMsg(self):
        return self.socketRep.recv_pyobj()

    def sendMsg(self, obj):
        return self.socketRep.send_pyobj(obj)

    def getAddress(self):
        return self.localAddress


class CommsClient:

    def __init__(self, target, port=5501):
        self.target = "tcp://" + target + ":" + str(port)
        self.ctx = zmq.Context()
        self.socketReq = self.ctx.socket(zmq.REQ)
        self.socketReq.connect(self.target)

    def recvMsg(self):
        return self.socketReq.recv_pyobj()

    def sendMsg(self, obj):
        return self.socketReq.send_pyobj(obj)

    def getTarget(self):
        return self.target