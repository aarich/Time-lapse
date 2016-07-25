from time import sleep
import picamera
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import sys

def timelapse(numPhotos, motorDur, waitTime):

	with picamera.PiCamera() as camera:
		camera.resolution = (1290, 1080)
		camera.start_preview()
		sleep(2)
		try:
			for i, filename in enumerate(camera.capture_continuous('image{counter:02d}.jpg')):
				print('Captured %s' % filename)
				if i == numPhotos:
					break
				# runMotor(motorDur)
				sleep(waitTime * 3600 - motorDur)
		finally:
			camera.stop_preview()

def runMotor(motorDur):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(25, GPIO.OUT)
	p = GPIO.PWM(25, 50)    # PWM on port 25 at 50 Hertz  
	p.start(50)             # start the PWM on 50 percent duty cycle  
	sleep(motorDur) 
	p.stop()

def main():
	if len(sys.argv) != 5:
		print "Usage:\n\n  sudo python " + sys.argv[0] + " delayToStart[hr] distToTravel[m] captureFreq[img/hr] duration[hr]"
		print "\nAll parameters must be greater than zero and can be floats."
		return

	delayToStart = float(sys.argv[1])
	distToTravel = float(sys.argv[2])
	captureFreq = float(sys.argv[3])
	duration = float(sys.argv[4])

	if True in map(lambda x: x <= 0, [distToTravel, captureFreq, duration]):
		print "Inputs must be positive (except for delayToStart). They can be floats."
		return

	# Sleep until start
	sleep(delayToStart * 3600)

	# determine motor run time after each photo
	motorConstant = 5 # units are s / m
	numPhotos = int(duration * captureFreq)
	motorDur = motorConstant * (distToTravel / numPhotos)

	# determine wait time after each photo
	waitTime = duration / numPhotos

	timelapse(numPhotos, motorDur, waitTime)

	GPIO.cleanup()

if __name__ == '__main__':
	main()