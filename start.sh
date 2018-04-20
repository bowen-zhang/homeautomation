#!/bin/bash

# Elevate privileges
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

LOG_PATH=/home/pi/src/logs
LOG_FILE=$LOG_PATH/start.log
SRC_PATH=/home/pi/src

check_process() {
	output=$(pgrep -f $1)
	[ $? -eq 1 ] && return 1 || return 0
}

log() {
	echo `date +"%Y/%m/%d %H:%M:%S"` $1 >> $LOG_FILE
	echo $1
}

[[ -d $LOG_PATH ]] || sudo -u pi mkdir -p $LOG_PATH

log "Start.sh"
check_process "main.py"
if [ $? -eq 0 ]; then
	echo 'Home automation is already running.'
else
	log "Disabling LED light..."
	sudo echo none | tee /sys/class/leds/led0/trigger

	log "Starting home automation..."
	cd $SRC_PATH/homeautomation
	sudo PYTHONPATH=$SRC_PATH -u pi python main.py > $LOG_PATH/log.stdout 2> $LOG_PATH/log.stderr &
	log "Home automation is running."
fi