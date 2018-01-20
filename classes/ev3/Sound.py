#!/usr/bin/env python3
from ev3dev.ev3 import *

class Sound:

    def beep():
        Sound.beep.wait()

    def doubleBeep():
        Sound.beep.wait()
        Sound.beep.wait()

    def tripleBeep():
        Sound.beep.wait()
        Sound.beep.wait()
        Sound.beep.wait()
        