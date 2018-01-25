#!/usr/bin/env python3
from ev3dev.ev3 import *

class Talk:

    def say(text):
        Sound.speak(text)

        