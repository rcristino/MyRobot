#!/usr/bin/env python3
from time import sleep

class Radar:

    DISTANCE = "dist#"

    def __init__(self, name, rate=0.1):
        self.name = name
        self.distance = 10

    def getName(self):
        return self.name

    def getDistance(self):
        return self.distance
