#!/usr/bin/env python
import unittest
import paho.mqtt.client as mqtt
import socket
from time import sleep

class TestClientMotor:

    def start_client(self):
        self.client = mqtt.Client()
        #self.client.connect(socket.gethostbyname(socket.gethostname()),1883,60)
        self.client.connect("ev3dev",1883,60)

    def set_speed(self, topic, speed):
        self.client.publish(topic, str(speed).encode(),0);

    def set_stop(self, topic):
        self.client.publish(topic, "stop".encode(),0);

    def stop_client(self):
        self.client.disconnect()


if __name__ == '__main__':
    #unittest.main()

    mClient = TestClientMotor()
    mClient.start_client()

    #self.assertEqual(mLeft.isConnected(), True)
    #self.assertEqual(mRight.isConnected(), True)

    mClient.set_speed("rick/mLeft", "move:200")
    mClient.set_speed("rick/mRight", "move:200")

    sleep(5)
    mClient.set_speed("rick/mLeft", "move:0")
    mClient.set_speed("rick/mRight", "move:0")

    sleep(1)
    mClient.set_stop("rick/mLeft")
    mClient.set_stop("rick/mRight")

    mClient.stop_client()
