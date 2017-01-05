#!/bin/bash

echo "Remove files from the remote directory"
ssh robot@ev3dev "rm -rf ~/ev3/$1"

echo "Copy files to the remote directory"
scp -r . robot@ev3dev:~/ev3/$1
