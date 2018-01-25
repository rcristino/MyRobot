#!/usr/bin/env python3
import os
from time import sleep
import speech_recognition as sr
from classes.CommsClients import CommsClientRobot
from classes.CommsClients import CommsClientGrabber
from classes.CommsClients import CommsClientMove

def listening():
    myText = ""
    # obtain audio from the microphone
    r = sr.Recognizer()
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

if __name__ == '__main__':

    ip_remote = os.environ['TARGET']
    robot = CommsClientRobot("robot", ip_remote, portCmd=5000)
    mLeft = CommsClientMove("motor_left", ip_remote, portCmd=5511, portEvt=5512)
    mRight = CommsClientMove("motor_right", ip_remote, portCmd=5521, portEvt=5522)
    grabber = CommsClientGrabber(ip_remote, portCmd=5501, portEvt=5502)
    sleep(3)

    isListening = True
    while(isListening):
        cmd = str(listening())
        if "say" in cmd:
            print("CMD: say")
            robot.action(cmd)
        if "move" in cmd:
            print("CMD: move")
            mLeft.action(100)
            mRight.action(100)
        if "reverse" in cmd:
            print("CMD: reverse")
            mLeft.action(-100)
            mRight.action(-100)
        elif "stop" in cmd:
            print("CMD: stop")
            mLeft.action(0)
            mRight.action(0)
        elif "left" in cmd:
            print("CMD: left")
            mLeft.action(-100)
            mRight.action(100)
            sleep(3)
            mLeft.action(0)
            mRight.action(0)            
        elif "right" in cmd:
            print("CMD: right")
            mLeft.action(100)
            mRight.action(-100)
            sleep(3)
            mLeft.action(0)
            mRight.action(0)            
        elif "open" in cmd:
            print("CMD: open")
            grabber.action(True)
        elif "close" in cmd:
            print("CMD: close")
            grabber.action(False)
        elif "shut down" in cmd:
            print("shut down")
            grabber.action(True)
            robot.action()
        elif "quit" in cmd:
            print("quit")
            grabber.action(True)
            isListening = False