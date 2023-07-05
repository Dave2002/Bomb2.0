import time

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(2,GPIO.OUT)



while True:
    GPIO.output(2,True)
    time.sleep(2)
    GPIO.output(2,False)
    time.sleep(2)