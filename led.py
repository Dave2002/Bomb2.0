# include all necessary packages to get LEDs to work with Raspberry Pi
import threading
import time
import board
import neopixel
import RPi.GPIO as GPIO


class Led:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)
        self._pixel = neopixel.NeoPixel(board.D18, 55, brightness=1)

        # Variabels for the LED Stripe Blinker
        self._stripeBlinkerThread = None
        self._stripeRGB = (0,0,0)
        self._stripeBlinkerStop = False
        self._stripeIntervall = 1
        self._stripeBlinkerIsAlive = False

        # Blue outside Blinker Variables
        self._blueBlinkerThread = None
        self._blueBlinkerStop = False
        self._blueBlinkerInterval = 1
        self._blueBlinkerIsAlive = False

        # Red outside Blinker Variables
        self._redBlinkerThread = None
        self._redBlinkerStop = False
        self._redBlinkerInterval = 1
        self._redBlinkerIsAlive = False

    # Simple stuff

    def stopAllBlinkers(self):
        self.stopRedBlinker()
        self.stopBlueBlinker()
        self.stopStripeBlinker()

    def turnOffAll(self):
        self.turnOffRed()
        self.pixelFill((0,0,0))
        self.turnOffBlue()


    def turnRedOn(self):
        GPIO.output(20, True)

    def turnBlueOn(self):
        GPIO.output(23, True)

    def turnOffBlue(self):
        GPIO.output(23, False)

    def turnOffRed(self):
        GPIO.output(20, False)

    def stripeOff(self):
        self._pixel.fill((0,0,0))

    def pixelFill(self,rgb):
        self._pixel.fill(rgb)
        self._stripeRGB = rgb


    # Blinker logic

    def getBlueIsAlive(self):
        return self._blueBlinkerIsAlive

    def getRedIsAlive(self):
        return self._redBlinkerIsAlive
    def setBlueInterval(self,interval):
        self._blueBlinkerInterval = interval

    def startBlueBlinker(self):
        self._blueBlinkerThread = threading.Thread(target=self._blueBlinker,daemon=True)
        self._blueBlinkerThread.start()
        self._blueBlinkerIsAlive = True
    def _blueBlinker(self):
        while not self._blueBlinkerStop:
            GPIO.output(23, True)
            time.sleep(self._blueBlinkerInterval/2)
            GPIO.output(23, False)
            time.sleep(self._blueBlinkerInterval/2)

    def stopBlueBlinker(self):
        self._blueBlinkerStop = True
        try:
            self._blueBlinkerThread.join()
        except Exception:
            pass
        self._blueBlinkerIsAlive = False
        self._blueBlinkerStop = False


    def setRedInterval(self,interval):
        self._redBlinkerInterval = interval


    def startRedBlinker(self):
        self._redBlinkerThread = threading.Thread(target=self._redBlinker,daemon=True)
        self._redBlinkerThread.start()
        self._redBlinkerIsAlive = True

    def _redBlinker(self):
        while not self._redBlinkerStop:
            GPIO.output(20, True)
            time.sleep(self._redBlinkerInterval/2)
            GPIO.output(20, False)
            time.sleep(self._redBlinkerInterval/2)

    def stopRedBlinker(self):
        self._redBlinkerStop = True
        try:
            self._redBlinkerThread.join()
        except Exception:
            pass
        self._redBlinkerStop = False
        self._redBlinkerIsAlive = False

    #Strip Blinker stuff

    def getStripBlinkerAlive(self):
        return self._stripeBlinkerIsAlive


    def setRGB(self,rgb):
        self._stripeRGB = rgb

    def setStripInterval(self,intervall):
        self._stripeIntervall = intervall

    def startStripeBlinker(self,pulse):
        if not pulse:
            self._stripeBlinkerThread = threading.Thread(target=self._stripeBlinker,daemon=True)
            self._stripeBlinkerThread.start()
        else:
            self._stripeBlinkerThread = threading.Thread(target=self._pulsStripe,daemon=True)
            self._stripeBlinkerThread.start()
        self._stripeBlinkerIsAlive = True

    def _pulsStripe(self):
        while not self._stripeBlinkerStop:
            tmp = [0, 0, 0]
            tmp[0] = self._stripeRGB[0]
            tmp[1] = self._stripeRGB[1]
            tmp[2] = self._stripeRGB[2]
            while sum(tmp) > 20:
                tmp[0] = min(tmp[0] - tmp[0] * 0.1, 255)
                tmp[1] = min(tmp[1] - tmp[1] * 0.1, 255)
                tmp[2] = min(tmp[2] - tmp[2] * 0.1, 255)
                time.sleep(0.1)
                self.pixelFill(list(tmp))
            while sum(tmp) < 250:
                tmp[0] = min(tmp[0] + tmp[0] * 0.1, 255)
                tmp[1] = min(tmp[1] + tmp[1] * 0.1, 255)
                tmp[2] = min(tmp[2] + tmp[2] * 0.1, 255)
                time.sleep(0.1)
                self.pixelFill(list(tmp))

    def stopStripeBlinker(self):
        self._stripeBlinkerStop = True
        try:
            self._stripeBlinkerThread.join()
        except Exception:
            pass
        self._stripeBlinkerStop = False
        self._stripeBlinkerIsAlive = False



    def _stripeBlinker(self):
        while not self._stripeBlinkerStop:
            self._pixel.fill(self._stripeRGB)
            time.sleep(self._stripeIntervall/2)
            self._pixel.fill((0,0,0))
            time.sleep(self._stripeIntervall/2)



"""

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

stop = False


def ledOutSideBlink(c):
    if c == "blue":
        outsideBlueOn()
        time.sleep(1)
        outsideBlueOff()
    else:
        outsideRedOn()
        time.sleep(1)
        outsideRedOff()


def outsideRedOn():
    GPIO.output(20, True)
    # 18 -> 20


def outsideRedOff():
    GPIO.output(20, False)


def outsideBlueOn():
    GPIO.output(23, True)


def outsideBlueOff():
    GPIO.output(23, False)


pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=1)


def green():
    pixels1.fill((0, 255, 0))
    print("test")


def red():
    pixels1.fill((255, 0, 0))


def blue():
    pixels1.fill((0, 0, 255))


def yellow():
    pixels1.fill((255, 255, 0))


def puls(intervall):
    for x in range(0, 250, intervall):
        pixels1.fill((0, x, 0))
        time.sleep(0.1)
    for g in range(250, 0, -intervall):
        pixels1.fill((0, x, 0))
        time.sleep(0.1)
    pixels1.fill((0, 0, 0))


def off():
    pixels1.fill((0, 0, 0))


def blink(intervall, color):
    while not stop:
        if color == "green":
            green()
        elif color == "red":
            red()
        elif color == "yellow":
            yellow()
        elif color == "blue":
            blue()
        time.sleep(intervall / 2)
        pixels1.fill((0, 0, 0))
        time.sleep(intervall / 2)


blink(1,"red")
"""
