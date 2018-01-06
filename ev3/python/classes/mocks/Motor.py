#!/usr/bin/env python3
from time import sleep

class Motor:

    #FIXME to be checked and deleted
    MOVE = "move#"
    STOP = "stop"
    STATE = "state#"

    def __init__(self, name, device_port, isLarge = True):
        self.speed = 0
        self.name = name
        self.device_port = device_port
        self.stop()

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def movePosition(self, position, speed, action="hold"):
        print("MOVE POSITION: Position: " + str(position) + " [" + self.name + "] Motor: " + self.device_port + " Speed: " + str(self.speed))

    def moveTime(self, speed, intime):
        print("MOVE TIME: intime: " + intime + " [" + self.name + "] Motor: " + self.device_port + " Speed: " + str(self.speed))

    def move(self, speed):
        self.speed = int(speed)
        print("MOVE: [" + self.name + "] Motor: " + self.device_port + " Speed: " + str(self.speed))

    def stopRelax(self):
        print("STOP RELAX: [" + self.name + "] Motor: " + self.device_port)

    def stop(self):
        print("STOP: [" + self.name + "] Motor: " + self.device_port)

    def waitWhileRunning(self):
        print("WAIT WHILE RUNNING: [" + self.name + "] Motor: " + self.device_port)
        sleep(3)

    def __str__(self):
        return "[" + self.name + "] Motor: " + self.device_port + " Speed: " + str(self.speed)
