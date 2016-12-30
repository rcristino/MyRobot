#!/usr/bin/env python3

class Motor:
    def __init__(self, name):
        self.speed = 0
        self.name = name
        self.motor = "Motor" + name
        self.direction = 1
        self.stop()
        print("[" + self.name + "] MotorMock create")

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed
        print("[" + self.name + "] setSeed: " + str(speed))

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        self.direction = direction
        print("[" + self.name + "] setDirection")

    def movePosition(self, position, speed, action="hold"):
        self.speed = speed * self.direction
        print("[" + self.name + "] " + str(speed))

    def moveTime(self, speed, intime):
        self.speed = speed * self.direction
        print("[" + self.name + "] " + str(speed))

    def move(self, speed):
        self.speed = speed * self.direction
        print("[" + self.name + "] " + str(speed))

    def stopRelax(self):
        print("[" + self.name + "] stopRelax")

    def stop(self):
        print("[" + self.name + "] stop")

    def wait(self):
        print("[" + self.name + "] wait")

    def __str__(self):
        return "[" + self.name + "] Motor: " + self.name + " Speed: " + str(self.speed)
