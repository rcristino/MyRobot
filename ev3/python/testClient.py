#!/usr/bin/env python
from classes.Comms import CommsClient
from classes.Comms import CommsSubcriber
from classes.Comms import Message
import argparse
import _thread
from time import sleep

class CommsClientGrabber:
    def __init__(self, target, portCmd=5501, portEvt=5502):
        self.target = target
        self.grabCommsClient = CommsClient(self.target, portCmd)
        self.grabCommsSub = CommsSubcriber(self.target, portEvt)
        print("Client Grabber CMDs connecting to: " + self.grabCommsClient.getTarget())
        print("Client Grabber EVTs connecting to: " + self.grabCommsSub.getTarget())
        _thread.start_new_thread(self.workerStatus, (0.1,))

    def action(self, toOpen):
        cmd = Message("grabber",toOpen)
        self.grabCommsClient.sendCmd(cmd)
        reply = self.grabCommsClient.recvCmdReply()
        print("Grabber command status: " + reply.getName() + " : " + str(reply.getValue()))

    def workerStatus(self, interval=0.1):
        while True:
            evt = self.grabCommsSub.recvEvt()
            print("Grabber event: " + evt.getName() + " -> " + str(evt.getValue()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_remote", help="IP address from the Robot (e.g. 127.0.0.1)")
    args = parser.parse_args()

    # connect to grabber
    grabber = CommsClientGrabber(args.ip_remote)

    sleep(3)
    print("close grabber")
    grabber.action(False)
    sleep(3)
    print("open grabber")
    grabber.action(True)
    sleep(3)
