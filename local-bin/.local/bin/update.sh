#!/bin/bash
sudo timeshift --check &&
paru -Syu &&
sudo flatpak update &&
sudo pacman -Rs $(pacman -Qtdq);
paccache -k 2 -r
