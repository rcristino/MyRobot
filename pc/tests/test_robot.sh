#!/bin/bash

export TARGET=$1
export PYTHONPATH=${PWD}/../..
python3 test_robot.py
