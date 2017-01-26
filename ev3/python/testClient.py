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
        self.state = {}
        if activeLog is not False:
            self.client.on_log = self.on_log
        _thread.start_new_thread(self.on_loop, (1, ))

    def stop_client(self):
        self.client.disconnect()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def send(self, topic, index, data = None):
        if data is None:
            self.client.publish(topic, str(index).encode(),0);
        else:
            self.client.publish(topic, str(str(index) + str(data)).encode(),0);

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        data = msg.payload.decode()
        # Display the status from robot
        print("[" + topic + "]: " + data)
        self.state[topic] = data

    def on_loop(self, targetAddress):
        self.client.loop_forever()

    def on_log(mosq, obj, level, s, string):
        print(string)

    def getData(self, topic):
        if (topic in self.state):
            return self.state[topic]


class TestClientMotor:

    def __init__(self, topic, commsClient):
        self.topic = topic
        self.commsClient = commsClient
        self.commsClient.subscribe(self.topic + "/status")

    def set_speed(self, speed):
        self.commsClient.send(self.topic, "move#", speed)

    def set_stop(self):
        self.commsClient.send(self.topic, "stop".encode(), 0);

class TestClientGrabber:

    def __init__(self, topic, commsClient):
        self.topic = topic
        self.commsClient = commsClient
        self.commsClient.subscribe(self.topic + "/status")

    def actionMove(self):
        self.commsClient.send(self.topic, "move")
        sleep(1)


if __name__ == '__main__':
    #unittest.main()
    commsClient = CommsClient("ev3dev")

    mLeftClient = TestClientMotor("rick/mLeft", commsClient)
    mRightClient = TestClientMotor("rick/mRight", commsClient)
    gClient = TestClientGrabber("rick/grabber", commsClient)

    #self.assertEqual(mLeft.isConnected(), True)
    #self.assertEqual(mRight.isConnected(), True)

    mLeftClient.set_speed(200)
    mRightClient.set_speed(200)

    sleep(5)

    gClient.actionMove()
    gClient.actionMove()

    sleep(5)

    mLeftClient.set_stop()
    mRightClient.set_stop()

    sleep(5)
    
    commsClient.stop_client()
