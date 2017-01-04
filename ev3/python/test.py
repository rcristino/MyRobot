#!/usr/bin/env python
import unittest
from classes.MotorMock import Motor
#from .classes.Motor import Motor
from classes.Comms import ServerComms
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


class TestServerMotor:

    def start_server(self):

        self.commsServer = ServerComms()
        self.commsServer.subcribe("mLeft","rick/mLeft")
        self.commsServer.subcribe("mRight","rick/mRight")
        #self.mLeft = Motor("outA")
        #self.mRight = Motor("outD")

    def printData(self):
        print(self.commsServer.getData("mLeft"))
        print(self.commsServer.getData("mRight"))

class TestStringMethods(unittest.TestCase):

    def test_motor_run(self):
        print("test")

if __name__ == '__main__':
    #unittest.main()
    mServer = TestServerMotor()
    mServer.start_server()

    sleep(2)

    mClient = TestClientMotor()
    mClient.start_client()

    sleep(2)
    mClient.set_speed("rick/mLeft", "move:500")
    mClient.set_speed("rick/mRight", "move:500")

    sleep(2)
    mServer.printData()

    #sleep(1)
    #mClient.set_stop("rick/mLeft")
    #mClient.set_stop("rick/mRight")

    mClient.stop_client()
