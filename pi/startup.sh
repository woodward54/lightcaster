#!/bin/sh
sleep 2
rm /home/pi/artnet.log
python /home/pi/artnet.py --brightness=50 -c > /home/pi/artnet.log 2>&1