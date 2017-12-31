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

    def recvMsg(self):
        return self.socketRep.recv_pyobj()

    def sendMsg(self, obj):
        self.socketRep.send_pyobj(obj)

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
        self.socketReq.send_pyobj(obj)

    def getTarget(self):
        return self.target


class CommsPublisher:

    def __init__(self, topic, port=5601):
        self.localAddress = "tcp://*:" + str(port)
        self.topic = topic
        self.ctx = zmq.Context()
        self.socketPub = self.ctx.socket(zmq.PUB)
        self.socketPub.bind(self.localAddress)

    def sendMsg(self, obj):
        self.socketPub.send_string(self.topic, zmq.SNDMORE)
        self.socketPub.send_pyobj(obj)

    def getAddress(self):
        return self.localAddress

    def getTopic(self):
        return self.topic


class CommsSubcriber:

    def __init__(self, target, topic, port=5601):
        self.target = "tcp://" + target + ":" + str(port)
        self.topic = topic
        self.ctx = zmq.Context()
        self.socketSub = self.ctx.socket(zmq.SUB)
        self.socketSub.setsockopt_string(zmq.SUBSCRIBE, self.topic)
        self.socketSub.connect(self.target)

    def recvMsg(self):
        topic = self.socketSub.recv_string()
        msg = self.socketSub.recv_pyobj()
        return msg

    def getTarget(self):
        return self.target

    def getTopic(self):
        return self.topic