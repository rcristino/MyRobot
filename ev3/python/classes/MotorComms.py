#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import socket
import _thread

class MotorComms:
    def __init__(self, topic, targetMotor):
        self.connection = False
        self.topic = topic
        self.targetMotor = targetMotor
        self.targetAddress = socket.gethostbyname(socket.gethostname())
        self.client = mqtt.Client()
        self.client.connect(self.targetAddress,1883,60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        _thread.start_new_thread(self.on_loop, (self.topic, ))

    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.topic = topic

    def setTargetMotor(self):
        self.targetMotor = targetMotor

    def isConnected(self):
        return self.connection

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connection = True
            self.client.subscribe(self.topic)
        else:
            print("Error: cannot receive connection or subscribe topic")

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        if data.find("move:") == 0:
            speed = int(data[len("move:"):])
            self.targetMotor.move(speed)
        elif data == "disconnect":
            self.targetMotor.stopRelax()
        elif data == "stop":
            self.targetMotor.stop()
        elif data == "wait":
            self.targetMotor.wait()
        else:
            print("Error: Unknown payload received")
        self.disconnect()

    def disconnect(self):
        self.client.disconnect()

    def on_loop(self, topic):
        self.client.loop_forever()
