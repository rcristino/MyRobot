#!/usr/bin/env python3
from ev3dev.ev3 import *

class Motor:
    def __init__(self, name):
        self.speed = 0
        self.name = name
        self.motor = LargeMotor(name)
        self.direction = 1
        self.stop()

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        self.direction = direction

    def movePosition(self, position, speed, action="hold"):
        self.speed = speed * self.direction
        self.motor.run_to_rel_pos(position_sp=position, speed_sp=self.speed, stop_action=action)

    def moveTime(self, speed, intime):
        self.speed = speed * self.direction
        self.motor.run_timed(time_sp=intime, speed_sp=self.speed)

    def move(self, speed):
        self.speed = speed * self.direction
        self.motor.run_forever(speed_sp=self.speed)

    def stopRelax(self):
        self.motor.stop(stop_action="coast")

    def stop(self):
        self.motor.stop(stop_action="hold")

    def wait(self):
        self.motor.wait_while('running')

    def __str__(self):
        return "[" + self.name + "] Motor: " + self.name + " Speed: " + str(self.speed)
