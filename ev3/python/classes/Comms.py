#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import socket
import _thread
import queue

class ServerComms:

    def __init__(self):
        self.connection = False
        self.targetAddress = socket.gethostbyname(socket.gethostname())
        self.client = mqtt.Client()
        self.client.connect(self.targetAddress,1883,60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subcribe = self.on_subcribe
        self.client.on_log = self.on_log
        self.topicDevice = {}
        self.deviceQueue = {}
        _thread.start_new_thread(self.on_loop, (self.targetAddress, ))

    def isConnected(self):
        return self.connection

    def subcribe(self, device, topic):
        self.topicDevice[topic] = device
        self.deviceQueue[device] = queue.Queue()

    def on_log(mosq, obj, level, s, string):
        print(string)

    def on_subcribe(mosq, obj, mid, granted_qos):
        print("Subcribed: " + str(mid)) + " " + str(granted_qos)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connection = True
            for topic, device in self.topicDevice.items():
                self.client.subscribe(topic)
        else:
            print("Error: cannot receive connection or subscribe topic")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        data = msg.payload.decode()
        device = self.topicDevice[topic]
        self.deviceQueue[device].put(data)

    def getData(self, device):
        data = ""
        if not self.deviceQueue[device].empty():
            data = self.deviceQueue[device].get()
        return data

    def disconnect(self):
        self.client.disconnect()

    def on_loop(self, targetAddress):
        self.client.loop_forever()
