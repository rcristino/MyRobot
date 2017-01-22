#!/usr/bin/env python
import unittest
import paho.mqtt.client as mqtt
import socket
from time import sleep
import _thread

class CommsClient:
    def __init__(self, targetAddress, activeLog = False):
        self.client = mqtt.Client()
        self.client.connect(targetAddress,1883,60)
        self.client.on_message = self.on_message
        if activeLog is not False:
            self.client.on_log = self.on_log
        self.client.subscribe("rick/status")
        _thread.start_new_thread(self.on_loop, (1, ))

    def stop_client(self):
        self.client.disconnect()

    def send(self, topic, index, data = None):
        if data is None:
            self.client.publish(topic, str(index).encode(),0);
        else:
            self.client.publish(topic, str(str(index) + str(data)).encode(),0);

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        data = msg.payload.decode()
        print(data)

    def on_loop(self, targetAddress):
        self.client.loop_forever()

    def on_log(mosq, obj, level, s, string):
        print(string)


class TestClientMotor:

    def __init__(self, commsClient):
        self.commsClient = commsClient

    def set_speed(self, topic, speed):
        self.commsClient.send(topic, "move#", speed)

    def set_stop(self, topic):
        self.commsClient.send(topic, "stop".encode(), 0);

class TestClientGrabber:

    def __init__(self, commsClient):
        self.commsClient = commsClient

    def actionOpen(self, topic):
        self.commsClient.send(topic, "open")

    def actionClose(self, topic):
        self.commsClient.send(topic, "close")

if __name__ == '__main__':
    #unittest.main()
    commsClient = CommsClient("ev3dev")

    mClient = TestClientMotor(commsClient)
    gClient = TestClientGrabber(commsClient)

    #self.assertEqual(mLeft.isConnected(), True)
    #self.assertEqual(mRight.isConnected(), True)

    mClient.set_speed("rick/mLeft", 200)
    mClient.set_speed("rick/mRight", 200)

    gClient.actionClose("rick/grabber")
    gClient.actionOpen("rick/grabber")


    sleep(15)
    mClient.set_stop("rick/mLeft")
    mClient.set_stop("rick/mRight")

    commsClient.stop_client()
