#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import _thread

class Display:
    def __init__(self):
        self.lcd = Screen()
        self.smile = True
        _thread.start_new_thread(self.displayWorker, (self.smile, ))

    def setSmile(self, isSmiling):
        self.smile = isSmiling

    def getSmile(self):
        return self.smile

    def displayWorker(self, smile):

        while True:
            self.lcd.clear()

            self.lcd.draw.ellipse(( 20, 20,  60, 60))
            self.lcd.draw.ellipse((118, 20, 158, 60))

            if self.smile:
                self.lcd.draw.arc((20, 80, 158, 100), 0, 180)
            else:
                self.lcd.draw.arc((20, 80, 158, 100), 180, 360)

            # Update lcd display
            self.lcd.update()
            sleep(1)
