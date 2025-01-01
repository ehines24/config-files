#!/bin/bash

if [ x"$@" = x"Exit" ]; then
        exit 0
fi
echo -en "\0prompt\x1fCustom script\n"
echo -e "Option 1\nOption 2\nOption 3\nExit"
