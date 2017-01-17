#!/usr/bin/env python3
from ev3dev.ev3 import *
from classes.Motor import Motor
from classes.Comms import ServerComms
from classes.Display import Display
from classes.Radar import Radar
from time import sleep
import _thread

class Rick:
    def __init__(self):
        print("RICK starting")

        # Motion and Display init
        self.disp = Display()

        self.mLeft = Motor("rick/mLeft", "outA")
        self.mRight = Motor("rick/mRight", "outD")
        self.grabber = Motor("rick/grabber", "outC", False)

        self.radar = Radar()

        # Comms Init
        self.commsServer = ServerComms()
        self.commsServer.subcribe(self.mLeft.getName())
        self.commsServer.subcribe(self.mRight.getName())

        _thread.start_new_thread(self.motorCommsWorker, (self.commsServer, self.mLeft))
        _thread.start_new_thread(self.motorCommsWorker, (self.commsServer, self.mRight))
        _thread.start_new_thread(self.radarCommsWorker, (self.commsServer, self.radar))

        Sound.beep().wait()
        print("RICK ready")

        #FIXME test grabber
        self.grabber.move(100)

    def motorCommsWorker(self, commsServer, motor):
        while(True):
            sleep(0.1)
            mData = self.commsServer.getData(motor.getName())
            if mData.find(Motor.MOVE) is not -1:
                speed = mData[len(Motor.MOVE):]
                motor.move(speed)

            if mData.find(Motor.STOP) is not -1:
                motor.stop()

            commsServer.send("rick/status", motor.STATE + motor.getName(), motor.getState())

    def radarCommsWorker(self, commsServer, radar):
        while(True):
            sleep(0.1)
            commsServer.send("rick/status", Radar.DISTANCE, radar.getDistance())

    def shutdown(self):
        print("RICK stopping")

        #FIXME test grabber
        self.grabber.stopRelax()

        self.mLeft.stopRelax()
        self.mRight.stopRelax()

        print("RICK stoped")

def main():

    try:
        Leds.set_color(Leds.LEFT, Leds.AMBER)
        Leds.set_color(Leds.RIGHT, Leds.AMBER)
        rick = Rick()
        sleep(60) ## FIXME to be removed
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
    except:
        Leds.set_color(Leds.LEFT, Leds.RED)
        Leds.set_color(Leds.RIGHT, Leds.RED)
        print("ERROR:", sys.exc_info()[0])
        raise
    finally:
        rick.shutdown()

if __name__ == "__main__":
    main()
