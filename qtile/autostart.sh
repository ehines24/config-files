#!/bin/bash
# x11: move screens into right positions
xrandr --output eDP-1 --auto --output HDMI-1 --auto --left-of eDP-1
# turn on compositor
picom &
