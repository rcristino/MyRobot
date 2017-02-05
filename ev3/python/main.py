#!/usr/bin/env python3
from ev3dev.ev3 import *
from classes.Logger import Logger
from classes.Motor import Motor
from classes.Grabber import Grabber
#from classes.Comms import ServerComms
from classes.Display import Display
from classes.Radar import Radar
from time import sleep
import _thread
import argparse

class Rick:
    def __init__(self):

        # Motion and Display init
        self.disp = Display()

        self.mLeft = Motor("rick/mLeft", "outA")
        self.mRight = Motor("rick/mRight", "outD")
        self.grabber = Grabber("rick/grabber", "outC")

        self.radar = Radar("rick/radar")

        # Comms Init
        #self.commsServer = ServerComms()
        #self.commsServer.subcribe(self.mLeft.getName())
        #self.commsServer.subcribe(self.mRight.getName())
        #self.commsServer.subcribe(self.grabber.getName())

        #_thread.start_new_thread(self.motorCommsWorker, (self.commsServer, self.mLeft))
        #_thread.start_new_thread(self.motorCommsWorker, (self.commsServer, self.mRight))
        #_thread.start_new_thread(self.grabberCommsWorker, (self.commsServer, self.grabber))
        #_thread.start_new_thread(self.statusCommsWorker, (self.commsServer, self.mLeft, self.mRight, self.grabber, self.radar))


    def statusCommsWorker(self, commsServer, mLeft, mRight, grabber, radar):
        while(True):
            sleep(0.1)
            commsServer.send(mLeft.getName() + "/status", mLeft.STATE, mLeft.getState())
            commsServer.send(mRight.getName() + "/status", mRight.STATE, mRight.getState())
            commsServer.send(grabber.getName() + "/status", grabber.STATE, grabber.getState())
            commsServer.send(radar.getName() + "/status", radar.DISTANCE, radar.getDistance())


    def motorCommsWorker(self, commsServer, motor):
        while(True):
            sleep(0.1)
            mData = self.commsServer.getData(motor.getName())
            if mData.find(Motor.MOVE) is not -1:
                speed = mData[len(Motor.MOVE):]
                motor.move(speed)

            if mData.find(Motor.STOP) is not -1:
                motor.stop()


    def grabberCommsWorker(self, commsServer, grabber):
        ts = TouchSensor();
        while(True):
            sleep(0.1)
            if(grabber.getState() is not "running"):
                mData = self.commsServer.getData(grabber.getName())
                if mData.find(Grabber.MOVE) is not -1:
                    grabber.move()
                elif(ts.value()):
                    grabber.move()


    def shutdown(self):

        if(self.grabber.getState() is "close"):
            self.grabber.move()

        self.grabber.stopRelax()

        self.mLeft.stopRelax()
        self.mRight.stopRelax()

        Sound.beep().wait()
        Sound.beep().wait()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("ip_remote", help="IP address from Control Center (e.g. 127.0.0.1)")
    args = parser.parse_args()
    try:
        Logger(args.ip_remote)
        Leds.set_color(Leds.LEFT, Leds.AMBER)
        Leds.set_color(Leds.RIGHT, Leds.AMBER)
        Logger.logInfo("RICK starting")
        rick = Rick()
        Logger.logInfo("RICK ready")
        Sound.beep().wait()

        sleep(60) ## FIXME to be removed

        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
    except:
        Leds.set_color(Leds.LEFT, Leds.RED)
        Leds.set_color(Leds.RIGHT, Leds.RED)
        Logger.logError(sys.exc_info()[0])
        Sound.beep().wait()
        Sound.beep().wait()
        Sound.beep().wait()
        raise
    finally:
        Logger.logInfo("RICK stopping")
        rick.shutdown()
        Logger.logInfo("RICK stoped")

if __name__ == "__main__":
    main()
