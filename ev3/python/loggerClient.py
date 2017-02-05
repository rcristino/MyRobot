#!/usr/bin/env python
import logging
import zmq
from zmq.log.handlers import PUBHandler
from time import sleep

def sub_logger(target="*", port=5558 , level=logging.DEBUG):
    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    print("Logger is binding to: tcp://" + str(target) + ":" + str(port))
    sub.bind("tcp://" + str(target) + ":" + str(port))
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    logging.basicConfig(level=level)

    while True:
        level, message = sub.recv_multipart()
        message = message.decode('ascii')
        if message.endswith('\n'):
            # trim trailing newline, which will get appended again
            message = message[:-1]
        log = getattr(logging, level.lower().decode('ascii'))
        log(message)


if __name__ == '__main__':
    sub_logger()
