#!/usr/bin/env python3
#from classes.MotorMock import Motor
from classes.Motor import Motor
from classes.Comms import ServerComms
from time import sleep
import _thread


def actionWorker(commsServer, mLeft, mRight):
    print("RICK listening")
    while(True):
        sleep(0.1)

        mLeftData = commsServer.getData("mLeft")
        mRightData = commsServer.getData("mRight")

        speedIdxLeft = mLeftData.find("move:")
        speedIdxRight = mRightData.find("move:")
        if speedIdxLeft is not -1:
            speed = mLeftData[len("move:"):]
            mLeft.move(speed)
        if speedIdxRight is not -1:
            speed = mRightData[len("move:"):]
            mRight.move(speed)
            
def main():
    print("RICK starting")

    mLeft = Motor("outA")
    mRight = Motor("outD")

    commsServer = ServerComms()
    commsServer.subcribe("mLeft","rick/mLeft")
    commsServer.subcribe("mRight","rick/mRight")

    _thread.start_new_thread(actionWorker, (commsServer, mLeft, mRight, ))


    sleep(60)

    mLeft.stopRelax()
    mRight.stopRelax()

    print("RICK stopping")


if __name__ == "__main__":
    main()
