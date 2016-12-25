#!/usr/bin/env python3

class Motor:
    def __init__(self, name):
        self.speed = 0
        self.name = name
        self.motor = "Motor" + name
        self.direction = 1
        self.stop()
        print("MotorMock")

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed
        print("setSeed: " + str(speed))

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        self.direction = direction
        print("setDirection")

    def movePosition(self, position, speed, action="hold"):
        self.speed = speed * self.direction
        print("movePosition: " + str(speed))

    def moveTime(self, speed, intime):
        self.speed = speed * self.direction
        print("moveTime: " + str(speed))

    def move(self, speed):
        self.speed = speed * self.direction
        print("move: " + str(speed))

    def stopRelax(self):
        print("stopRelax")

    def stop(self):
        print("stop")

    def wait(self):
        print("wait")

    def __str__(self):
        return "Motor: " + self.name + " Speed: " + str(self.speed)
        
