#!/bin/bash

echo "Copy files to the remote directory"
scp -r . robot@ev3dev:~/ev3/$1
