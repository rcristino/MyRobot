#!/usr/bin/env python
import unittest
import argparse
import _thread
from time import sleep
import os
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

    def getReply(self):
        return self.reply

    def getEvent(self):
        return self.evt

    def action(self, toOpen):
        cmd = Message(self.name,toOpen)
        self.grabCommsClient.sendCmd(cmd)
        self.reply = self.grabCommsClient.recvCmdReply()
        print("Grabber command status: " + self.reply.getName() + " : " + str(self.reply.getValue()))

    def workerStatus(self, interval=0.1):
        while True:
            self.evt = self.grabCommsSub.recvEvt()
            print("Grabber event: " + self.evt.getName() + " -> " + str(self.evt.getValue()))


class CommsClientMove:
    def __init__(self, name, target, portCmd=5511, portEvt=5512):
        self.target = target
        self.name = name
        self.moveCommsClient = CommsClient(self.target, "test_move_cmd", portCmd)
        self.moveCommsSub = CommsSubcriber(self.target, "test_move_evt", portEvt)
        print("Client Move CMDs connecting to: " + self.moveCommsClient.getTarget())
        print("Client Move EVTs connecting to: " + self.moveCommsSub.getTarget())
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def getReply(self):
        return self.reply

    def getEvent(self):
        return self.evt

    def action(self, speed):
        cmd = Message(self.name, speed)
        self.moveCommsClient.sendCmd(cmd)
        self.reply = self.moveCommsClient.recvCmdReply()
        print("Move command status: " + self.reply.getName() + " : " + str(self.reply.getValue()))

    def workerStatus(self, interval=0.1):
        while True:
            self.evt = self.moveCommsSub.recvEvt()
            print("Move event: " + self.evt.getName() + " -> " + str(self.evt.getValue()))

class CommsClientRadar:
    def __init__(self, name, target, portEvt=5532):
        self.target = target
        self.name = name
        self.radarCommsSub = CommsSubcriber(self.target, "test_radar_evt", portEvt)
        print("Client Radar EVTs connecting to: " + self.radarCommsSub.getTarget())
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def getEvent(self):
        return self.evt

    def workerStatus(self, interval=0.1):
        while True:
            self.evt = self.radarCommsSub.recvEvt()
            print("Radar event: " + self.evt.getName() + " -> " + str(self.evt.getValue()))


class TestRobot(unittest.TestCase):

    def setUp(self):
        self.ip_remote = os.environ['TARGET']

    def test_radar(self):
        radar = CommsClientRadar("radar", self.ip_remote, portEvt=5532)
        print("»» PUT HAND IN FRONT OF THE RADAR ««")
        sleep(3)

        self.assertEqual(radar.getEvent().getName(), "radar")
        self.assertTrue(radar.getEvent().getValue() > 0)

    def test_grabber(self):
        grabber = CommsClientGrabber(self.ip_remote, portCmd=5501, portEvt=5502)
        sleep(3)
        
        # close grabber
        grabber.action(False)
        sleep(3)
        self.assertEqual(grabber.getReply().getName(), "grabber")
        self.assertEqual(grabber.getReply().getValue(), True)
        self.assertEqual(grabber.getEvent().getName(), "grabber")
        self.assertEqual(grabber.getEvent().getValue(), "close")

        # open grabber
        grabber.action(True)
        self.assertEqual(grabber.getReply().getName(), "grabber")
        self.assertEqual(grabber.getReply().getValue(), True)
        self.assertEqual(grabber.getEvent().getName(), "grabber")
        self.assertEqual(grabber.getEvent().getValue(), "open")

    def test_motor(self):
        mLeft = CommsClientMove("motor_left", self.ip_remote, portCmd=5511, portEvt=5512)
        mRight = CommsClientMove("motor_right", self.ip_remote, portCmd=5521, portEvt=5522)

        sleep(3)
        mLeft.action(100)
        mRight.action(100)
        sleep(3)

        self.assertEqual(mLeft.getReply().getName(), "motor_left")
        self.assertEqual(mLeft.getReply().getValue(), True)
        self.assertEqual(mLeft.getEvent().getName(), "motor_left")
        self.assertEqual(mLeft.getEvent().getValue(), "move")

        self.assertEqual(mRight.getReply().getName(), "motor_right")
        self.assertEqual(mRight.getReply().getValue(), True)
        self.assertEqual(mRight.getEvent().getName(), "motor_right")
        self.assertEqual(mRight.getEvent().getValue(), "move")

        mLeft.action(0)
        mRight.action(0)
        sleep(3)

        self.assertEqual(mLeft.getReply().getName(), "motor_left")
        self.assertEqual(mLeft.getReply().getValue(), True)
        self.assertEqual(mLeft.getEvent().getName(), "motor_left")
        self.assertEqual(mLeft.getEvent().getValue(), "stop")

        self.assertEqual(mRight.getReply().getName(), "motor_right")
        self.assertEqual(mRight.getReply().getValue(), True)
        self.assertEqual(mRight.getEvent().getName(), "motor_right")
        self.assertEqual(mRight.getEvent().getValue(), "stop")

if __name__ == '__main__':
    unittest.main()