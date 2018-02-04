#!/usr/bin/env python3
from classes.CommsClients import CommsClientRobot
from classes.CommsClients import CommsClientGrabber
from classes.CommsClients import CommsClientMove
from classes.CommsClients import CommsClientRadar
from classes.CommsClients import commsClientTerminate
import os
from time import sleep
import speech_recognition as sr
import _thread
import traceback

def listening():
    myText = ""
    # obtain audio from the microphone
    r = sr.Recognizer()
    r.pause_threshold = 0.5 # minimum length of silence (in seconds) that will register as the end of a phrase
    r.dynamic_energy_threshold = True # or sounds should be automatically adjusted based on the currently ambient noise level while listening
    with sr.Microphone() as source:
    #with sr.Microphone(device_index=3) as source:
        print("listening...")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        myText = r.recognize_google(audio)
        print("Interpreted: " + myText)
        return myText
    except sr.UnknownValueError:
        pass #print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def checkDistance(rate=0.1):
    maxDistance = 30 #cm
    radar = CommsClientRadar("radar", ip_remote, portEvt=5532)
    sleep(3) # wait for comms init

    while True:
        if radar.getEvent().getName() == "radar" and radar.getEvent().getValue() < maxDistance:
            mLeft.action(0)
            mRight.action(0)
        sleep(rate)

def collectVoiceCmds(rate=0.1):
    while(True):
        stackVoiceCmds.append(str(listening())) # wait and add voice commands in the stack

def voiceHandler(rate=0.1):

    speed = 200
    isListening = True

    robot.action("at your command!")

    while(isListening):
        if stackVoiceCmds:
            cmd = stackVoiceCmds.pop() # get voice commands from stack
        else:
            cmd = ""

        if "say" in cmd:
            print("CMD: say")
            robot.action(cmd[len("say"):]) # remove say from the string
        elif "move" in cmd:
            print("CMD: move")
            mLeft.action(speed)
            mRight.action(speed)
        elif "reverse" in cmd:
            print("CMD: reverse")
            mLeft.action(speed * -1)
            mRight.action(speed * -1)
        elif "stop" in cmd:
            print("CMD: stop")
            mLeft.action(0)
            mRight.action(0)
        elif "left" in cmd:
            print("CMD: left")
            mLeft.action((speed * -1) / 2)
            mRight.action(speed / 2)
        elif "right" in cmd:
            print("CMD: right")
            mLeft.action(speed / 2)
            mRight.action((speed * -1) / 2)
        elif "open" in cmd:
            print("CMD: open")
            grabber.action(True)
        elif "close" in cmd:
            print("CMD: close")
            grabber.action(False)
        elif "shut down" in cmd:
            print("shut down")
            grabber.action(True)
            mLeft.action(0)
            mRight.action(0)
            robot.action("goodbye!")
            robot.action()
            commsClientTerminate()
            isListening = False
        elif "quit" in cmd:
            print("quit")
            grabber.action(True)
            mLeft.action(0)
            mRight.action(0)
            commsClientTerminate()
            isListening = False
        sleep(rate)

if __name__ == '__main__':

    try:
        ip_remote = os.environ['TARGET']
        robot = CommsClientRobot("robot", ip_remote, portCmd=5000)
        mLeft = CommsClientMove("motor_left", ip_remote, portCmd=5511, portEvt=5512)
        mRight = CommsClientMove("motor_right", ip_remote, portCmd=5521, portEvt=5522)
        grabber = CommsClientGrabber(ip_remote, portCmd=5501, portEvt=5502)
        
        stackVoiceCmds = []
        _thread.start_new_thread(collectVoiceCmds, (0.1,))
        _thread.start_new_thread(checkDistance, (0.1,))

        voiceHandler()
    except:
        print(traceback.format_exc())
    finally:
        commsClientTerminate()