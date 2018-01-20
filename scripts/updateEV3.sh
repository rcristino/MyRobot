#!/bin/bash

echo "Check if mntEV3 has been mounted!"
echo "Remove content from ../mntEV3/ev3"
rm -rf ../mntEV3/ev3/*
echo "Copy content to ../mntEV3/ev3"
cp -r ../ev3 ../mntEV3/ev3/
cp -r ../classes ../mntEV3/ev3/
