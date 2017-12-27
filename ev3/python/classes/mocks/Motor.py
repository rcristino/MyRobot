#!/usr/bin/env python3

class Motor:

    MOVE = "move#"
    STOP = "stop"
    STATE = "state#"

    def __init__(self, name, port, isLarge = True):
        self.speed = 0
        self.name = name
        self.port = port
        self.stop()

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def movePosition(self, position, speed, action="hold"):
        print("MOVE POSITION: Position: " + position + "[" + self.name + "] Motor: " + self.port + " Speed: " + str(self.speed))

    def moveTime(self, speed, intime):
        print("MOVE TIME: intime: " + intime + "[" + self.name + "] Motor: " + self.port + " Speed: " + str(self.speed))

    def move(self, speed):
        self.speed = int(speed)
        print("MOVE: [" + self.name + "] Motor: " + self.port + " Speed: " + str(self.speed))

    def stopRelax(self):
        print("STOP RELAX: [" + self.name + "] Motor: " + self.port)

    def stop(self):
        print("STOP: [" + self.name + "] Motor: " + self.port)

    def waitWhileRunning(self):
        print("WAIT WHILE RUNNING: [" + self.name + "] Motor: " + self.port)

    def getState(self):
        return "mock_running"

    def __str__(self):
        return "[" + self.name + "] Motor: " + self.port + " Speed: " + str(self.speed)
