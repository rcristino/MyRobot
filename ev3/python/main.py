#!/usr/bin/env python3
from ev3dev.ev3 import *
from classes.Motor import Motor
from classes.Comms import ServerComms
from classes.Display import Display
from time import sleep
import _thread

class Rick:
    def __init__(self):
        print("RICK starting")

        self.disp = Display()

        self.mLeft = Motor("outA")
        self.mRight = Motor("outD")

        self.commsServer = ServerComms()
        self.commsServer.subcribe(self.mLeft.getName(),"rick/mLeft")
        self.commsServer.subcribe(self.mRight.getName(),"rick/mRight")

        _thread.start_new_thread(self.motorWorker, (self.commsServer, self.mLeft, ))
        _thread.start_new_thread(self.motorWorker, (self.commsServer, self.mRight, ))

        Sound.beep().wait()

    def motorWorker(self, commsServer, motor):
        while(True):
            sleep(0.1)

            mData = self.commsServer.getData(motor.getName())

            speedIdx = mData.find("move:")
            if speedIdx is not -1:
                speed = mData[len("move:"):]
                motor.move(speed)

            stopIdx = mData.find("stop")
            if stopIdx is not -1:
                motor.stop()

    def shutdown(self):
        mLeft.stopRelax()
        mRight.stopRelax()

        print("RICK stopping")

def main():

    rick = Rick()

    sleep(60)

    rick.shutdown()




if __name__ == "__main__":
    main()
