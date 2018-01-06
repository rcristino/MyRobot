#!/usr/bin/env python3
from time import sleep
from classes.mocks.Motor import Motor
from classes.Comms import CommsServer
from classes.Comms import CommsPublisher
from classes.Comms import Message

class Move(Motor):

    MOVE = "move#"
    STOP = "stop"
    STATE = "state#"

    def __init__(self, name, device_port):
        Motor.__init__(self, name, device_port, True)
        self.speed = 0
        self.name = name
        self.device_port = device_port
        self.state = "stop"
        self.stop()

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def movePosition(self, position, speed, action="hold"):
        print("MOVE POSITION: Position: " + str(position) + " [" + self.name + "] Motor: " + self.port + " Speed: " + str(self.speed))
        self.state = "running"

    def moveTime(self, speed, intime):
        print("MOVE TIME: intime: " + intime + " [" + self.name + "] Motor: " + self.device_port + " Speed: " + str(self.speed))
        self.state = "running"

    def move(self, speed):
        self.speed = int(speed)
        print("MOVE: [" + self.name + "] Motor: " + self.device_port + " Speed: " + str(self.speed))
        self.state = "running"

    def stopRelax(self):
        print("STOP RELAX: [" + self.name + "] Motor: " + self.device_port)
        self.state = "stop"

    def stop(self):
        print("STOP: [" + self.name + "] Motor: " + self.device_port)
        self.state = "stop"

    def waitWhileRunning(self):
        print("WAIT WHILE RUNNING: [" + self.name + "] Motor: " + self.device_port)
        self.state = "waiting"
        sleep(3)

    def getState(self):
        return self.state

    def __str__(self):
        return "[" + self.name + "] Move: " + self.device_port + " Speed: " + str(self.speed)
