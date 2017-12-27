#!/usr/bin/env python3
from classes.Logger import Logger
from time import sleep
import _thread
import argparse

class Rick:
    def __init__(self):

        # Motion and Display init
        self.disp = Display()

        #self.mLeft = Motor("rick/mLeft", "outA")
        #self.mRight = Motor("rick/mRight", "outD")
        self.grabber = Grabber("rick/grabber", "outC")

        #self.radar = Radar("rick/radar")


    # TODO update this method to report status as events
    def statusCommsWorker(self, commsServer, mLeft, mRight, grabber, radar):
        while(True):
            sleep(0.1)
            commsServer.send(mLeft.getName() + "/status", mLeft.STATE, mLeft.getState())
            commsServer.send(mRight.getName() + "/status", mRight.STATE, mRight.getState())
            commsServer.send(grabber.getName() + "/status", grabber.STATE, grabber.getState())
            commsServer.send(radar.getName() + "/status", radar.DISTANCE, radar.getDistance())


    def shutdown(self):

        if(self.grabber.getState() is "close"):
            self.grabber.move()

        self.grabber.stopRelax()

        #self.mLeft.stopRelax()
        #self.mRight.stopRelax()

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
        Logger.logError(sys.exc_info()[0])
        Sound.tripleBeep()
        raise
    finally:
        Logger.logInfo("RICK stopping")
        rick.shutdown()
        Logger.logInfo("RICK stoped")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_remote", help="IP address from Control Center (e.g. 127.0.0.1)")
    parser.add_argument("--mocks", help="Enable Mocks fuctionaloty for development purpose (e.g. --mocks True)")
    parser.argument_default
    args = parser.parse_args()

    if(args.mocks):
        from classes.mocks.Motor import Motor
        from classes.mocks.Grabber import Grabber
        from classes.mocks.Display import Display
        from classes.mocks.Radar import Radar
        from classes.mocks.Sound import Sound
        from classes.mocks.Led import Led
    else:
        from classes.ev3.Motor import Motor
        from classes.ev3.Grabber import Grabber
        from classes.ev3.Display import Display
        from classes.ev3.Radar import Radar
        from classes.ev3.Sound import Sound
        from classes.ev3.Led import Led
    
    startup(args)
