gifbox
======

Little Python/Tornado server that cycles through gifs, plus instructions for how to set it up to launch automatically in Chromium on a Raspberry Pi 


###Install Instructions

1. Use SDFormatter to format SD card (at least 8GB, more likely 16GB)
1. Download NOOBS (http://www.raspberrypi.org/downloads/)
1. Extract files
1. Copy NOOB files to SD card
1. Boot up PI
1. Set internationalization options in raspi-config
1. Login: pi/raspberry
1. `sudo apt-get update`
1. `sudo apt-get upgrade`
1. Remote desktop: `sudo apt-get install xrdp`
1. Filesharing `sudo apt-get install netatalk`
1. [change hostname to something useful](http://www.howtogeek.com/167195/how-to-change-your-raspberry-pi-or-other-linux-devices-hostname/)
	1. `sudo nano /etc/hosts`
	1. `sudo nano /etc/hostname`
	1. `sudo /etc/init.d/hostname.sh`
	1. `sudo reboot`
1. [Set up Bonjour/ZeroConf](http://www.raspberrypi.org/forums/viewtopic.php?f=66&t=18207) `sudo apt-get install libnss-mdns` ([or this one](http://www.howtogeek.com/167190/how-and-why-to-assign-the-.local-domain-to-your-raspberry-pi/)?)
1. [Make sure composite video works](http://elinux.org/R-Pi_Troubleshooting#Composite_displays_no_image) 
	1. Is the Pi configuration forcing HDMI output? Inspect the file "config.txt" in the boot partition of your memory card and look for the line "hdmi_force_hotplug=1". If you see this line, comment it out (in particular, look at the end of "config.txt", in the section entitled "NOOBS Auto-generated Settings:")
1. Install pip 
	1. `sudo apt-get install python-setuptools`
	1. `sudo easy_install pip`
	1. `sudo pip install tornado`

## Fullsreen browser at boot
1. Install Chromium browser `sudo apt-get install chromium`
1. Make a directory for Chromium `mkdir /home/pi/.chromium`

>     #!/bin/sh
>     xset -dpms     # disable DPMS (Energy Star) features.
>     xset s off       # disable screen saver
>     xset s noblank # don't blank the video device
>     unclutter &
>     matchbox-window-manager -use_titlebar no -use_cursor no &
>     chromium  --user-data-dir=/home/pi/.chromium --app="http://gifpi.local:8888" > /home/pi/chromium.log 2>&1
>     #midori -e Fullscreen -a "http://gifpi.local:8888" > /home/pi/midori.log 2>&1


1. Copy tornado gif server to home folder
1. edit `/etc/rc.local`
1. add the lines before exit 0

>		python /home/pi/tornato/app.py &
>		sudo xinit /home/pi/startBrowser &

(sources: [one*](http://www.ediy.com.my/index.php/blog/item/102-raspberry-pi-running-midori-browser-without-a-desktop), [two](http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/gui/auto-run-browser-on-startup), [three](http://www.instructables.com/id/Raspberry-Pi-Digital-Signage-Exchange-Rate-Display/step13/Start-the-Midori-browser-in-full-screen-mode/))
* ended up using #one



## Install Node (not using node any more)

1. [Install from download instead of apt-get](http://raspberryalphaomega.org.uk/2014/06/11/installing-and-using-node-js-on-raspberry-pi/)
	1. Make sure to add /opt/node/bin to PATH
1. [Here is the latest arm-compatible version as of Oct 15 2014: node-v0.10.3-linux-arm-pi.tar.gz](http://nodejs.org/dist/v0.10.3/node-v0.10.3-linux-arm-pi.tar.gz)
1. [if you get "Error: No compatible version found"...](https://github.com/npm/npm/issues/4984)
1. [if you get "Error: failed to fetch from registry"...](http://stackoverflow.com/questions/12913141/installing-from-npm-fails)
1. To install pm2
	1. `sudo env PATH=$PATH npm install -g --unsafe-perm pm2`



