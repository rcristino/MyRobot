#!/usr/bin/env python
from classes.Comms import CommsClient
from classes.Comms import Message
import argparse

class CommsClientGrabber:
    def __init__(self, target, port=5501):
        self.grabCommsClient = CommsClient(target, port)
        print("Client Grabber connecting to: " + self.grabCommsClient.getTarget())

    def action(self, toOpen):
        msg = Message("grabber",toOpen)
        self.grabCommsClient.sendMsg(msg)
        reply = self.grabCommsClient.recvMsg()
        print("Grabber command status: " + reply.getName() + " : " + str(reply.getValue()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_remote", help="IP address from the Robot (e.g. 127.0.0.1)")
    args = parser.parse_args()

    # connect to grabber
    grabber = CommsClientGrabber(args.ip_remote)

    print("close grabber")
    grabber.action(False)

    print("open grabber")
    grabber.action(True)
