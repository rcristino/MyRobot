# rick project #

### (work in progress...) ###

## Context ##
rick project is a sandbox where some ideas are implemented about different
interfaces, workflow, communication, commands and events handling, etc.

Devices:
* EV3 (Lego Mindstorm): EV3 is running debian destribution called: [ev3dev](http://www.ev3dev.org)
* VM (Ubuntu): It is a normal Virtual Machine running Ubuntu 16.04 LTS

Libraries:
* ev3python: basing this development on python3, this python API is being used: [ev3python](https://sites.google.com/site/ev3python)
* pyzmq: for the communication between Robot (EV3) and Controller (VM),
zmq has been integrated, by using synchronous communication (REQ/REP)
and asynchronous (PUB/SUB). For more details: [pyzmq](https://pyzmq.readthedocs.io/en/latest/index.html)

### Road map ###

* All components in the Robot are handler by the Controller (VM)
* Events status are handler by the Controller
* Create Leap Motion handler and integrate it with the Controller
(command the robot with hands moves). More details can be found here: [leapmotion.com](https://www.leapmotion.com/)
* Create voice command handler and integrate it with the Controller.
Perhaps using [snowboy](https://snowboy.kitt.ai/)

## Author ##
[Ricardo Cristino](https://de.linkedin.com/in/ricardo-cristino-0b95b74)
