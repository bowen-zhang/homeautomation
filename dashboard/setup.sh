#!/bin/bash

# Elevate privileges
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

#Set up auto start
sudo cp homeautomation.sh /etc/init.d/homeautomation
sudo update-rc.d homeautomation defaults