#!/usr/bin/env python
import zmq
import socket
from time import sleep
import _thread
import argparse

class CommsClientGrabber:
    def __init__(self, target, port=5501):
        self.target = "tcp://" + target + ":" + str(port)
        self.ctx = zmq.Context()
        self.socketReq = self.ctx.socket(zmq.REQ)
        self.socketReq.connect(self.target)
        print("Client Grabber connecting to: " + self.target)

    def actionMove(self):
        self.socketReq.send_string("move")
        status = self.socketReq.recv_string()
        print("Move command status: " + status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_remote", help="IP address from the Robot (e.g. 127.0.0.1)")
    args = parser.parse_args()

    # connect to grabber
    grabber = CommsClientGrabber(args.ip_remote)

    print("close grabber")
    grabber.actionMove()

    print("open grabber")
    grabber.actionMove()
