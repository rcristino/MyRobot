#!/usr/bin/env python
import unittest
import _thread
from time import sleep
import os
from classes.CommsClients import CommsClientGrabber
from classes.CommsClients import CommsClientMove
from classes.CommsClients import CommsClientRadar
from classes.CommsClients import CommsClientRobot

class TestRobot(unittest.TestCase):

    def setUp(self):
        self.ip_remote = os.environ['TARGET']

    def test_rabot(self):
        robot = CommsClientRobot("robot", self.ip_remote, portCmd=5000)
        sleep(3)

        self.assertEqual(robot.getReply().getName(), "robot")
        self.assertEqual(robot.getReply().getValue(), True)

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