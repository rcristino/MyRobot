#!/usr/bin/env python3
import socket
if( socket.gethostname() == "ev3dev"):
    from classes.ev3.Display import Display
    from classes.ev3.Beep import Beep
    from classes.ev3.Led import Led
else:
    from classes.mocks.Display import Display
    from classes.mocks.Beep import Beep
    from classes.mocks.Led import Led
from classes.Logger import Logger
from classes.Move import Move
from classes.Grabber import Grabber
from classes.Radar import Radar
from classes.Comms import commsTerminate
import traceback
from time import sleep
import _thread
import argparse
import zmq

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
    
        commsTerminate()

        Beep.doubleBeep()


def startup(args):

    try:
        Logger()
        Led.amber()
        Logger.logInfo("RICK starting")
        rick = Rick()
        Logger.logInfo("RICK ready")
        Beep.singleBeep()
        Led.green()

        sleep(60) ## FIXME to be removed

    except:
        Led.red()
        Logger.logError(traceback.format_exc().splitlines())
        Beep.tripleBeep()
    finally:
        Logger.logInfo("RICK stopping")
        rick.shutdown()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.argument_default
    args = parser.parse_args()
    
    startup(args)
