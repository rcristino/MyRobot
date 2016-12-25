#!/usr/bin/env python3
from .MotorMock import Motor
#from .Motor import Motor
import paho.mqtt.client as mqtt

class MotorComms(Motor):
    def __init__(self, topic, targetMotor):
        Motor.__init__(self, targetMotor)
        self.topic = topic
        self.targetMotor = targetMotor

    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.topic = topic

    def setTargetMotor(self):
        self.targetMotor = targetMotor
