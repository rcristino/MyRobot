#!/usr/bin/env python3
import sys
if('ev3dev' in sys.modules):
    from classes.ev3.Display import Display
    from classes.ev3.Sound import Sound
    from classes.ev3.Led import Led
else:
    from classes.mocks.Display import Display
    from classes.mocks.Sound import Sound
    from classes.mocks.Led import Led
from classes.Logger import Logger
from classes.Move import Move
from classes.Grabber import Grabber
from classes.Radar import Radar
import traceback
from time import sleep
import _thread
import argparse

class Rick:
    def __init__(self):

        # Motion and Display init
        self.disp = Display()

        self.mLeft = Move("motor_left", "outA", portCmd=5511, portEvt=5512)
        self.mRight = Move("motor_right", "outD", portCmd=5521, portEvt=5522)
        self.grabber = Grabber("grabber", "outC", portCmd=5501, portEvt=5502)

        self.radar = Radar()


    def shutdown(self):

        if(self.grabber.getState() is "close"):
            self.grabber.move()

        self.grabber.stopRelax()

        self.mLeft.stopRelax()
        self.mRight.stopRelax()

        Sound.doubleBeep()


def startup(args):

    try:
        Logger(args.ip_remote)
        Led.amber()
        Logger.logInfo("RICK starting")
        rick = Rick()
        Logger.logInfo("RICK ready")
        Sound.beep()

        sleep(60) ## FIXME to be removed

        Led.green()
    except:
        Led.red()
        Logger.logError(traceback.format_exc().splitlines())
        Sound.tripleBeep()
    finally:
        Logger.logInfo("RICK stopping")
        rick.shutdown()
        Logger.logInfo("RICK stoped")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_remote", help="IP address from Control Center (e.g. 127.0.0.1)")
    parser.argument_default
    args = parser.parse_args()
    
    startup(args)
