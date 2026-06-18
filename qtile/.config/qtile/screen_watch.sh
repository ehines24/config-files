#!/bin/bash
DISPLAY_COUNT=0
sleep 5
while true; do
        LAST_DISPLAY_COUNT=$DISPLAY_COUNT
        DISPLAY_COUNT=$(xrandr | grep " connected" | wc -l)
        if (( $DISPLAY_COUNT != $LAST_DISPLAY_COUNT && $DISPLAY_COUNT != 0)) ; then
                qtile cmd-obj -o cmd -f restart
        fi
        sleep 5
done
