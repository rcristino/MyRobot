#!/usr/bin/env python
import argparse
import _thread
from time import sleep
import os
import logging
import sys
sys.path.append("../")
from classes.Comms import CommsClient
from classes.Comms import CommsSubcriber
from classes.Comms import Message

class CommsClientGrabber:
    def __init__(self, target, portCmd=5501, portEvt=5502):
        self.target = target
        self.name = "grabber"
        self.grabCommsClient = CommsClient(self.target, "test_grabber_cmd", portCmd)
        self.grabCommsSub = CommsSubcriber(self.target, "test_grabber_evt", portEvt)
        print("Client Grabber CMDs connecting to: " + self.grabCommsClient.getTarget())
        print("Client Grabber EVTs connecting to: " + self.grabCommsSub.getTarget())
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def action(self, toOpen):
        cmd = Message(self.name,toOpen)
        self.grabCommsClient.sendCmd(cmd)
        reply = self.grabCommsClient.recvCmdReply()
        print("Grabber command status: " + reply.getName() + " : " + str(reply.getValue()))

    def workerStatus(self, interval=0.1):
        while True:
            evt = self.grabCommsSub.recvEvt()
            print("Grabber event: " + evt.getName() + " -> " + str(evt.getValue()))


class CommsClientMove:
    def __init__(self, name, target, portCmd=5511, portEvt=5512):
        self.target = target
        self.name = name
        self.moveCommsClient = CommsClient(self.target, "test_move_cmd", portCmd)
        self.moveCommsSub = CommsSubcriber(self.target, "test_move_evt", portEvt)
        print("Client Move CMDs connecting to: " + self.moveCommsClient.getTarget())
        print("Client Move EVTs connecting to: " + self.moveCommsSub.getTarget())
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def action(self, speed):
        cmd = Message(self.name, speed)
        self.moveCommsClient.sendCmd(cmd)
        reply = self.moveCommsClient.recvCmdReply()
        print("Move command status: " + reply.getName() + " : " + str(reply.getValue()))

    def workerStatus(self, interval=0.1):
        while True:
            evt = self.moveCommsSub.recvEvt()
            print("Move event: " + evt.getName() + " -> " + str(evt.getValue()))

class CommsClientRadar:
    def __init__(self, name, target, portEvt=5532):
        self.target = target
        self.name = name
        self.radarCommsSub = CommsSubcriber(self.target, "test_radar_evt", portEvt)
        print("Client Radar EVTs connecting to: " + self.radarCommsSub.getTarget())
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def workerStatus(self, interval=0.1):
        while True:
            evt = self.radarCommsSub.recvEvt()
            print("Radar event: " + evt.getName() + " -> " + str(evt.getValue()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_remote", help="IP address from the Robot (e.g. 127.0.0.1)")
    args = parser.parse_args()

    # connect to each device e.g grabber
    grabber = CommsClientGrabber(args.ip_remote, portCmd=5501, portEvt=5502)
    mLeft = CommsClientMove("motor_left", args.ip_remote, portCmd=5511, portEvt=5512)
    mRight = CommsClientMove("motor_right", args.ip_remote, portCmd=5521, portEvt=5522)
    radar = CommsClientRadar("radar", args.ip_remote, portEvt=5532)

    sleep(3)
    print("test to close grabber")
    grabber.action(False)
    sleep(3)
    print("test to open grabber")
    grabber.action(True)
    sleep(3)
    print("test to move")
    mLeft.action(100)
    mRight.action(100)
    sleep(3)
    print("test to stop move")
    mLeft.action(0)
    mRight.action(0)
    sleep(3)