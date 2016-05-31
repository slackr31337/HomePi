#!/bin/bash
# echo "sudo /home/pi/startup.sh &" > /etc/rc.local; sudo chmod 755 /etc/rc.local

sleep 10

cd /home/pi
while true; do
        sudo /home/pi/homepi.py
done

