#!/bin/bash
export TARGET=$1
export PYTHONPATH=${PWD}/../..
python3 loggerClient.py
