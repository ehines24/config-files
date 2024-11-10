#!/bin/bash
count=$(ps aux | grep [s]pice-vdagent | wc -l)
echo $count
if (( $count > 1 )); then
	echo "Agent is running"
else 
	echo "Agent is not running"
	spice-vdagent &
	disown
fi
xrandr --output Virtual-1 --auto
xrandr --output Virtual-1 --auto
echo "fired off at $(date)" >> autostart_fired
