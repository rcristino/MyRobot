#!/usr/bin/env python3
import socket
if( socket.gethostname() == "ev3dev"):
    from classes.ev3.Display import Display
    from classes.ev3.Beep import Beep
    from classes.ev3.Talk import Talk
    from classes.ev3.Led import Led
else:
    from classes.mocks.Display import Display
    from classes.mocks.Beep import Beep
    from classes.mocks.Talk import Talk
    from classes.mocks.Led import Led
from classes.Comms import CommsServer
from classes.Comms import Message
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

class Robot:
    def __init__(self):
        self.name = "robot"
        self.isActive = True

        self.disp = Display()

        self.mLeft = Move("motor_left", "outA", portCmd=5511, portEvt=5512)
        self.mRight = Move("motor_right", "outD", portCmd=5521, portEvt=5522)
        self.grabber = Grabber("grabber", "outC", portCmd=5501, portEvt=5502)

        self.radar = Radar()

        self.mainCommsServer = CommsServer(self.name + "_cmd", port=5000) 
        _thread.start_new_thread(self.mainCommsWorker, (0.1,))

    def getIsActive(self):
        return self.isActive

    def mainCommsWorker(self, interval=0.1):
        while(self.isActive):
            cmd = self.mainCommsServer.recvCmd()
            if cmd.getName() == self.name and cmd.getValue() == "shutdown":
                replyCmd = Message(self.name, True)
                self.mainCommsServer.sendCmdReply(replyCmd)
                self.isActive = False
            elif cmd.getName() == self.name:
                replyCmd = Message(self.name, True)
                self.mainCommsServer.sendCmdReply(replyCmd)
                Talk.say(cmd.getValue())
            else:
                replyCmd = Message(self.name, False)
                self.mainCommsServer.sendCmdReply(replyCmd)
        self.shutdown()
        commsTerminate()


    def shutdown(self):

        if(self.grabber.getState() is "close"):
            self.grabber.move()

        self.grabber.stopRelax()

        self.mLeft.stopRelax()
        self.mRight.stopRelax()

        Beep.doubleBeep()


def startup(args):

    try:
        isActive = True

        Logger()
        Led.amber()
        Logger.logInfo("ROBOT starting")
        robot = Robot()
        Logger.logInfo("ROBOT ready")
        Beep.singleBeep()
        Led.green()

        while(robot.getIsActive()):
            sleep(1) 

    except:
        Led.red()
        Logger.logError(traceback.format_exc().splitlines())
        Beep.tripleBeep()
    finally:
        Logger.logInfo("ROBOT stopping")
        isActive = False

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.argument_default
    args = parser.parse_args()
    
    startup(args)
