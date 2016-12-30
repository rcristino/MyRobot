#!/usr/bin/env python
import unittest
from classes.MotorComms import MotorComms
import paho.mqtt.client as mqtt
import socket
from time import sleep

class TestClientMotor:

    def start_client(self):
        self.client = mqtt.Client()
        self.client.connect(socket.gethostbyname(socket.gethostname()),1883,60)

    def set_speed(self, topic, speed):
        self.client.publish(topic, str(speed).encode(),0);

    def set_stop(self, topic):
        self.client.publish(topic, "stop".encode(),0);

    def stop_client(self):
        self.client.disconnect()


class TestServerMotor(unittest.TestCase):

    def test_motor_run(self):

        mLeft = MotorComms("rick/mLeft","outA")
        mRight = MotorComms("rick/mRight","outD")

        mClient = TestClientMotor()
        mClient.start_client()

        #self.assertEqual(mLeft.isConnected(), True)
        #self.assertEqual(mRight.isConnected(), True)

        mClient.set_speed("rick/mLeft", "speed:500")
        mClient.set_speed("rick/mRight", "speed:500")

        sleep(5)

        mClient.set_stop("rick/mLeft")
        mClient.set_stop("rick/mRight")

        mClient.stop_client()

        mLeft.disconnect()
        mRight.disconnect()

        self.assertEqual(mLeft.isConnected(), False)
        self.assertEqual(mRight.isConnected(), False)


if __name__ == '__main__':
    unittest.main()
