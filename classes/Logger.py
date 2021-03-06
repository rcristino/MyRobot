
import logging
import zmq
from zmq.log.handlers import PUBHandler
from time import sleep
from multiprocessing import Process
import queue
import os
import _thread

class Logger:

    LOG_LEVELS = (logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL)
    isInit = False
    logQueue = queue.Queue()

    def __init__(self, port=5500, level=logging.DEBUG):
        if Logger.isInit is False:
            self.port = port
            self.level = level
            Logger.isInit = True
            _thread.start_new_thread(self.log_worker, (self.port,))
            sleep(1) # it gives time to have the connection ready

    def log_worker(self, port):
        ctx = zmq.Context()
        pub = ctx.socket(zmq.PUB)
        print("Logger: tcp://*:" + str(port))
        pub.bind("tcp://*:" + str(port))
        logger = logging.getLogger(str(os.getpid()))
        logger.setLevel(self.level)
        handler = PUBHandler(pub)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        ### console logging 
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # ch.setFormatter(formatter)
        # logger.addHandler(ch)

        while Logger.isInit:
            # wait for data in queue
            data = Logger.logQueue.get()
            level = data[0]
            message = data[1]
            logger.log(level, message)

    def terminate(self):
        Logger.isInit = False

    def logDebug(message):
        if Logger.isInit is True:
            data = [logging.DEBUG, message]
            Logger.logQueue.put(data)

    def logInfo(message):
        if Logger.isInit:
            data = [logging.INFO, message]
            Logger.logQueue.put(data)

    def logError(message):
        if Logger.isInit:
            data = [logging.ERROR, message]
            Logger.logQueue.put(data)
