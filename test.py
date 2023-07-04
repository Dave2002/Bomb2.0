import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

while True:
    GPIO.output(18, True)
    GPIO.output(23, True)
    time.sleep(2)
    GPIO.output(18, False)
    GPIO.output(23, False)
    time.sleep(2)