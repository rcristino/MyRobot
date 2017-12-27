#!/usr/bin/env python3


class Display:
    def __init__(self):
        self.smile = True

    def setSmile(self, isSmiling):
        self.smile = isSmiling
        if self.smile:
            print("DISPLAY SMILE")
        else:
            print("DISPLAY SAD")

    def getSmile(self):
        return self.smile
