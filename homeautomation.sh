#!/bin/sh
# /etc/init.d/homeautomation

### BEGIN INIT INFO
# Provides:				HomeAutomation
# Required-Start:
# Required-Stop:
# Default-Start:		2 3 4 5
# Default-Stop:			0 1 6
# Short-Description:	HomeAutomation initscript
# Description:			This service manages home automation
### END INIT INFO


case "$1" in
	start)
		sudo /home/pi/src/homeautomation/start.sh 0
		;;
	stop)
		sudo /home/pi/src/homeautomation/stop.sh
		;;
	*)
		echo "Usage: /etc/init.d/homeautomation start|stop"
		exit 1
		;;
esac

exit 0