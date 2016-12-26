

#!/usr/bin/env python

import paho.mqtt.client as mqtt
import socket

# This is the Publisher

client = mqtt.Client()
client.connect(socket.gethostbyname(socket.gethostname()),1883,60)
client.publish("topic/test", "Hello world!".encode(),0);
client.disconnect();
