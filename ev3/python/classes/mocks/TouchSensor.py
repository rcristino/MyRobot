#!/usr/bin/env python3

class TouchSensor:

    def __init__(self):
        print("TOUCH SENSOR INIT")

    def value(self):
        t = False
        # t = bool(random.getrandbits(1))
        if t:
            print("TOUCHED")
            return True
        else:
            return False