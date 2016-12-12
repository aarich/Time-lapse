from time import sleep, time
import picamera
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import sys
import os

MOTOR_SPEED = 500
MOTOR_RADIUS = 0.04 # supposedly cm
MOTOR_PINS = [23, 24, 25, 12]
COUNTS_PER_REV = 4600 #512

BACK = True

def timelapse(numPhotos, distBetweenPhotos, waitTime):
    GPIO.setmode(GPIO.BCM)
    for pin in MOTOR_PINS:
        print "Setting pin", pin, "to output."
        GPIO.setup(pin, GPIO.OUT)
        
    print "Beginning Timelapse:"
    print "Taking", numPhotos, "photos."
    print "Traveling", distBetweenPhotos, " m between photos"
    print "Waiting", waitTime, "hrs between photos"
    with picamera.PiCamera() as camera:
        camera.led = False
        camera.resolution = (1920, 1080)
        camera.start_preview()
        sleep(2)

        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = "off"
        g = camera.awb_gains
        camera.awb_mode = "off"
        camera.awb_gains = g
        try:
            for i, filename in enumerate(camera.capture_continuous('image{counter:04d}.jpg')):
                print('Captured %s' % filename)
                if i == numPhotos:
                    break
                start = time()
                runMotor(distBetweenPhotos)
                if waitTime * 3600 > numPhotos * 0.6:
                    showRemaining(numPhotos - i, camera)
                if waitTime * 3600 - (time() - start) > 0:
                    sleep(waitTime * 3600 - (time() - start))
        finally:
            camera.stop_preview()
    os.system("avconv -f image2 -i image%04d.jpg -r 12 tl.avi")
            

def showRemaining(photosRemaining, camera):
    for i in range(photosRemaining):
        camera.led = True
        sleep(0.4)
        camera.led = False
        sleep(0.1)

def runMotor(distance):
    print "Running Motor:"
    numRevs = distance / (2 * MOTOR_RADIUS * 3.1415)
    print "Number of Revolutions:", numRevs
    
    count = 0
    while count < COUNTS_PER_REV * numRevs:
        if BACK:
            setOutput((8 - count) % 8)
        else:
            setOutput(count % 8)
        sleep(MOTOR_SPEED / 100000.0)
        count = count + 1

def setOutput(output):
    pinVals = ["1000", "1100", "0100", "0110", "0010", "0011", "0001", "1001"]
    for pin in range(len(MOTOR_PINS)):
        GPIO.output(MOTOR_PINS[pin], pinVals[output][pin] == "1")

def testMotor():
    GPIO.setmode(GPIO.BCM)
    
    for pin in MOTOR_PINS:
        print "Setting pin", pin, "to output."
        GPIO.setup(pin, GPIO.OUT)

    distance = 0.1
    numRevs = distance / (2 * MOTOR_RADIUS * 3.1415)
    count = 0
    print "STARTING to do ", numRevs, "revolutions."
    while True:
        if sys.argv[1] == "b":
            setOutput(count % 8)
        else:
            setOutput((8 - count) % 8)
        sleep(MOTOR_SPEED / 100000.0)
        count = count + 1
        if count > COUNTS_PER_REV * numRevs:
            break

def main():
    if len(sys.argv) == 2:
        testMotor()
    if len(sys.argv) != 5:
        print "Usage:\n\nsudo python " + sys.argv[0] + " delayToStart[hr] distToTravel[cm] captureFreq[img/hr] duration[hr]"
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
    print "Waiting to start"
    sleep(delayToStart * 3600)

    # determine distance to travel
    numPhotos = int(duration * captureFreq)
    distBetweenPhotos = 1.0 * distToTravel / numPhotos

    waitTime = duration / numPhotos
    
    timelapse(numPhotos, distBetweenPhotos, waitTime)

    GPIO.cleanup()

if __name__ == '__main__':
    try:
        # Remove Old Files
        os.system("rm image*.jpg");
        os.system("rm tl.avi");
        main()
    except:
        print "Error:", sys.exc_info()
        pass
    print "cleaning Up"
    GPIO.cleanup()
