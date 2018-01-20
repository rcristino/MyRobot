#!/usr/bin/env python3
from ev3dev.ev3 import *

class Motor:

    MOVE = "move#"
    STOP = "stop"
    STATE = "state#"

    def __init__(self, name, port, isLarge = True):
        self.speed = 0
        self.name = name
        if isLarge:
            self.motor = LargeMotor(port)
        else:
            self.motor = MediumMotor(port)
        self.stop()

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def movePosition(self, position, speed, action="hold"):
        self.motor.run_to_rel_pos(position_sp=position, speed_sp=self.speed, stop_action=action)

    def moveTime(self, speed, intime):
        self.motor.run_timed(time_sp=intime, speed_sp=self.speed)

    def move(self, speed):
        self.speed = int(speed)
        self.motor.run_forever(speed_sp=self.speed)

    def stopRelax(self):
        self.motor.stop(stop_action="coast")

    def stop(self):
        self.motor.stop(stop_action="hold")

    def waitWhileRunning(self):
        self.motor.wait_while('running')

    def getState(self):
        return self.motor.state

    def __str__(self):
        return "[" + self.name + "] Motor: " + self.port + " Speed: " + str(self.speed)
