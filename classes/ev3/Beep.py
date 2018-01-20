#!/usr/bin/env python3
from ev3dev.ev3 import *

class Beep:

    def singleBeep():
        Sound.beep()

    def doubleBeep():
        Sound.beep()
        Sound.beep()

    def tripleBeep():
        Sound.beep()
        Sound.beep()
        Sound.beep()
        