#!/bin/bash
PATH=/bin:/usr/bin:/usr/local/bin
tl="/media/pi/ALEX RICH/tl"
suffix=".avi"
if [ -e "$tl$suffix" ]
then
	for i in `seq 1 10`;
	do
		if [ ! -e "$tl$i$suffix" ]
		then
			cp ~/Time-lapse/tl.avi "$tl$i$suffix"
			echo "Copying "$tl$i$suffix
			break
		fi
		echo "$tl$i$suffix"
	done
else
	echo "Copying "$tl$suffix
	cp ~/Time-lapse/tl.avi "$tl$suffix"
fi
