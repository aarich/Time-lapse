from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta
import sys

def main():
	if sys.argc < NUMARGS:
		print "Expected usage:\n\tsudo python " + argv[0] + "delayToStart[hr] distToTravel[m] captureFreq[img/hr] speed[m/hr]"

def wait():
    # Calculate the delay to the start of the next hour
    next_hour = (datetime.now() + timedelta(0, 3600)).replace(
        minute=0, second=0, microsecond=0)
    delay = (next_hour - datetime.now()).seconds
    sleep(delay)

camera = PiCamera()
camera.start_preview()
wait()
for filename in camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M}.jpg'):
    print('Captured %s' % filename)
    wait()

if __name__ == '__main__':
	main()