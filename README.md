# MyRobot project #

MyRobot project is a sandbox where some ideas are implemented about different
interfaces, workflows, communication, commands, events handling, etc.

List of functionalities:
* voice command to move forwards, backwards, left and right
* using IR as a radar to measure the distance. If obstacle is ahead, then it will stop
* a small wheel pointing up on the robot, it is a button. When it is pressed,  it will open or close the gripper
* it is possible to have a logger tool connected and observe remotely all commands, events and current robot state

![alt text](https://github.com/rcristino/MyRobot/blob/master/MyRobot.jpg)

Note: the cable attached is a power cable to avoid using batteries.

Devices:
* EV3 (Lego Mindstorm): EV3 is running debian destribution called: [ev3dev](http://www.ev3dev.org)
* VM (Ubuntu): It is a normal Virtual Machine running Ubuntu 16.04 LTS

Libraries:
* ev3python: basing this development on python3, this python API is being used: [ev3python](https://sites.google.com/site/ev3python)
* pyzmq: for the communication between the robot (EV3) and controller (VM),
zmq has been integrated, by using synchronous communication (REQ/REP)
and asynchronous (PUB/SUB). For more details: [pyzmq](https://pyzmq.readthedocs.io/en/latest/index.html)
* SpeechRecognition (PyPI): library which can convert voice to text. It uses a microphone and Google Speech recognition API. [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/)


## Repository Structure ##

* classes: location of all python classes
    - ev3: all classes interfacing with the real ev3python library
    - mocks: the same classes as ev3 but without ev3python dependencies to allow development and testing without real EV3
* ev3: starting point to run this program in EV3
* pc: location of all remote programs to command EV3
    - cvoice: program allows to drive EV3 by voice command
    - logger: it connects to the EV3 remotely and monitors all commands and events received and the general state
    - tests: based on unit tests, remotely they perform a quick check if all basic funtionalities are operating well
* scripts: list of scripts which are helpful for development


## Install & run ##

Make sure all libraries above are deployed in your EV3 (with ev3dev) and in your VM (ubuntu).

Make sure the EV3 is succesfully connected to the wireless network.

In VM using sshfs, mount a directory to become easy to transfer files between these two devices (VM and EV3).

    VM > mkdir mntEV3
    VM > cd scripts
    VM > ./mountEV3.sh (type VM super user password)

    Note: before switching off EV3 do not forget to umount
    VM > umount mntEV3 (type VM super user password)

Deploy the main program into EV3

    VM > cd scripts
    VM > ./updateEV3.sh (make sure ~/ev3 directory already exists in EV3)

Access the EV3 to start the program

    VM > cd scripts
    VM > ./sshEV3 (type ev3dev password)
    EV3 > cd ev3/ev3
    EV3 > ./run.sh (when it is ready, it beeps and shows a smile on the display)


### Example 1 ###

Test if all basic functionalities are operating well.

    VM > cd pc/tests
    VM > ./test_robot.sh ev3dev


### Example 2 ###

Command robot by voice

    VM > cd pc/cvoice
    VM > ./cvoice.sh ev3dev
    
    voice commands:
    "move" (move forwards)
    "reverse" (move backwards)
    "stop" (stop moving)
    "right" (turn right)
    "left" (turn left)
    "open" (open the gripper)
    "close" (close the gripper)
    "quit" (quit the cvoice program)
    "say I am on the way" (the rebot speaks "I am on the way")


## Video ##

[command robot by voice (cvoice)](https://www.youtube.com/watch?v=8Yo0Ii8pzM4)


## Author ##

[Ricardo Cristino](https://de.linkedin.com/in/ricardo-cristino-0b95b74)
